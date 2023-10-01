import logging
import pickle
from pathlib import Path
from typing import List, Union

import numpy as np
from scipy.stats import kurtosis, skew

from .main import Collage

logger = logging.getLogger()

logger.info("Collage feature extraction")

descriptors = [
    "AngularSecondMoment",  # 0
    "Contrast",  # 1
    "Correlation",  # 2
    "SumOfSquareVariance",  # 3
    "SumAverage",  # 4
    "SumVariance",  # 5
    "SumEntropy",  # 6
    "Entropy",  # 7
    "DifferenceVariance",  # 8
    "DifferenceEntropy",  # 9
    "InformationMeasureOfCorrelation1",  # 10
    "InformationMeasureOfCorrelation2",  # 11
    "MaximalCorrelationCoefficient",  # 12
]


def compute_collage3d(
    image: np.ndarray, mask: np.ndarray, haralick_windows: List[int]
) -> np.ndarray:
    feats = {}

    try:
        collage = Collage(
            image,
            mask,
            svd_radius=5,
            verbose_logging=True,
            num_unique_angles=64,
            haralick_window_size=haralick_windows,
        )

        collage_feats = collage.execute()

        print("Collage feats shape", collage_feats.shape)

        for collage_idx, descriptor in enumerate(descriptors):
            print(f"Processing collage {descriptor}")
            for orientation in range(2):
                feat = collage_feats[:, :, :, collage_idx, orientation].flatten()
                feat = feat[~np.isnan(feat)]

                feats[f"col_des_{descriptor}_ori_{orientation}"] = [
                    feat.mean(),
                    feat.std(),
                    skew(feat),
                    kurtosis(feat),
                ]

    except ValueError as err:
        print(f"VALUE ERROR- {err}")

    except Exception as err:
        print(f"EXCEPTION- {err}")

    return feats


def significant_slice_idx_data(mask_bool) -> tuple:
    """_summary_

    Args:
        mask_bool (_type_): _description_

    Returns:
        tuple: _description_
    """
    z_sum = np.sum(mask_bool, axis=(0, 1))

    most_value_slices = np.argsort(z_sum)[::-1]

    num_nonzero_slices = np.count_nonzero(z_sum)

    most_value_nonzero_slices = most_value_slices[:num_nonzero_slices]

    return most_value_nonzero_slices, num_nonzero_slices


def collage3d(
    image: np.ndarray,
    mask: np.ndarray,
    window_sizes: List[int],
    save_path,
    out_name: str,
    padding: Union[bool, int] = False,
) -> None:
    """
    Process a 3D image and its associated mask using a collage method with
    specified window sizes, and save the resulting features.

    Parameters:
    -----------
    image : np.ndarray
        The 3D image data to be processed.

    mask : np.ndarray
        The 3D mask data associated with the image.

    window_sizes : List[int]
        A list of window sizes for which the collage method will be applied.

    save_path : str or Path
        The directory path where the resulting features will be saved.

    out_name : str
        The base name used in the saved feature files.

    padding : Union[bool, int], optional (default=False)
        If provided and set to True, padding of 11 is applied. If an integer is provided,
        it determines the amount of padding around the most significant slices in the mask.
        No padding is applied if set to False.

    Returns:
    --------
    None

    Notes:
    ------
    - The resulting features will be saved in two formats: `.pkl` and `.npy`.
    - The names of the saved files will contain the `out_name` and window size.
    """
    if padding:
        if isinstance(padding, bool):
            padding = 11

        most_value_nonzero_slices, _ = significant_slice_idx_data(mask)
        min = most_value_nonzero_slices.min() - padding
        max = most_value_nonzero_slices.max() + padding
        print(f"min: {min}, max: {max}")

        mask = mask[:, :, min:max]
        image = image[:, :, min:max]

    for ws in window_sizes:
        print(f"Processing collage with window size {ws}")
        feats = compute_collage3d(
            image,
            mask,
            haralick_windows=ws,
        )

        print("Final stats", feats)

        if not Path(save_path).exists():
            Path(save_path).mkdir(parents=True, exist_ok=True)

        save_path_pickle = Path(save_path) / f"Feats_Col_{out_name}_ws_{ws}.pkl"
        save_path_npy = Path(save_path) / f"Feats_Col_{out_name}_ws_{ws}.npy"

        with open(save_path_pickle, "wb") as file:
            pickle.dump(feats, file)
        np.save(save_path_npy, feats)
