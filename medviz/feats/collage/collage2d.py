import logging
import pickle
from pathlib import Path
from typing import List

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


def compute_collage(
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

        print(collage_feats.shape)

        for collage_idx, descriptor in enumerate(descriptors):
            print(f"Processing collage {descriptor}")
            feat = collage_feats[:, :, collage_idx].flatten()
            feat = feat[~np.isnan(feat)]

            feats[f"col_des_{descriptor}"] = [
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


def collage2d(
    image: np.ndarray,
    mask: np.ndarray,
    window_sizes: List[int],
    save_path,
    out_name: str,
):
    """_summary_collage2d
    Compute collage features for a given image and mask.
    :param image: image to compute collage features for
    :type image: np.ndarray
    :param mask: mask to compute collage features for
    :type mask: np.ndarray
    :param window_sizes: window sizes to compute collage features for
    :type window_sizes: List[int]
    :param save_path: path to save collage features
    :type save_path: str
    :param out_name: name of output collage features
    :type out_name: str

    """
    for ws in window_sizes:
        feats = compute_collage(
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
