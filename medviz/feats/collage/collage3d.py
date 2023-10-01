import logging
import pickle
from pathlib import Path

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


def compute_collage(image, mask, haralick_windows):
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


def collage3d(image, mask, window_sizes, save_path, out_name):
    for ws in window_sizes:
        print(f"Processing collage with window size {ws}")
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
