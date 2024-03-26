import logging
import pickle
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kurtosis, skew

from .main import Collage, HaralickFeature

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


def compute_collage2d(
    image: np.ndarray,
    mask: np.ndarray,
    haralick_windows: int,
    feature_maps=False,
    save_path_feature_maps=None,
    save_raw_path=False,
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

        if save_raw_path:
            np.save(save_raw_path, collage_feats)

        if feature_maps:
            which_features = [
                HaralickFeature.AngularSecondMoment,
                HaralickFeature.Contrast,
                HaralickFeature.Correlation,
                HaralickFeature.SumOfSquareVariance,
                HaralickFeature.SumAverage,
                HaralickFeature.SumVariance,
                HaralickFeature.SumEntropy,
                HaralickFeature.Entropy,
                HaralickFeature.DifferenceVariance,
                HaralickFeature.DifferenceEntropy,
                HaralickFeature.InformationMeasureOfCorrelation1,
                HaralickFeature.InformationMeasureOfCorrelation2,
                HaralickFeature.MaximalCorrelationCoefficient,
            ]

            alpha = 0.5
            extent = 0, image.shape[1], 0, image.shape[0]

            for which_feature in which_features:
                collage_output = collage.get_single_feature_output(which_feature)

                figure = plt.figure(figsize=(15, 15))
                plt.imshow(image, cmap=plt.cm.gray, extent=extent)
                plt.imshow(collage_output, cmap=plt.cm.jet, alpha=alpha, extent=extent)

                figure.axes[0].get_xaxis().set_visible(False)
                figure.axes[0].get_yaxis().set_visible(False)

                plt.title(f"Feature map: {which_feature.name}")

                save_path_name = f"{save_path_feature_maps}_{which_feature.name}.png"
                plt.savefig(save_path_name)
                plt.close()

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
    feature_maps=False,
    save_raw=False,
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
        if not Path(save_path).exists():
            Path(save_path).mkdir(parents=True, exist_ok=True)

        save_path_pickle = Path(save_path) / f"Feats_Col_{out_name}_ws_{ws}.pkl"
        save_path_npy = Path(save_path) / f"Feats_Col_{out_name}_ws_{ws}.npy"
        save_path_feature_maps = Path(save_path) / f"FeatureMaps_{out_name}_ws_{ws}"

        save_raw_path = (
            Path(save_path) / f"Raw_{out_name}_ws_{ws}.npy" if save_raw else False
        )

        feats = compute_collage2d(
            image,
            mask,
            haralick_windows=ws,
            feature_maps=feature_maps,
            save_path_feature_maps=save_path_feature_maps,
            save_raw_path=save_raw_path,
        )
        print("Final stats", feats)

        with open(save_path_pickle, "wb") as file:
            pickle.dump(feats, file)
        np.save(save_path_npy, feats)
