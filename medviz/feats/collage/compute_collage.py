import numpy as np
from scipy.stats import kurtosis, skew

from .main import Collage


def compute_collage(
    image, mask, haralick_windows=[3, 5, 7, 9, 11], raw_save_path=None, name=None
):
    """This method computes Collage features

    Args:
        image (path object): path of image
        mask (path object): path of mask
        haralick_windows (list, optional): Kernel window size. Defaults to [3, 5, 7, 9, 11].

    Returns:
        numpy array: mean, standard deviation, skewness, and kurtosis of COLLAGE features based on kernel size and orientation
    """
    windows_length = len(haralick_windows)

    feats = np.zeros((13 * windows_length * 2, 4), dtype=np.double)

    for window_idx, haralick_window_size in enumerate(haralick_windows):
        try:
            collage = Collage(
                image,
                mask,
                svd_radius=5,
                verbose_logging=True,
                num_unique_angles=64,
                haralick_window_size=haralick_window_size,
            )

            collage_feats = collage.execute()
            if raw_save_path:
                raw_file_path = (
                    raw_save_path / f"{name}_COLLAGE_RAW_W{haralick_window_size}.npy"
                )

                np.save(
                    raw_file_path,
                    collage_feats,
                )
                print("saved")

            for orientation in range(2):
                for collage_idx in range(13):
                    k = window_idx * collage_idx * orientation
                    feat = collage_feats[:, :, :, collage_idx, orientation].flatten()
                    feat = feat[~np.isnan(feat)]

                    feats[k, 0] = feat.mean()
                    feats[k, 1] = feat.std()
                    feats[k, 2] = skew(feat)
                    feats[k, 3] = kurtosis(feat)

        except ValueError as err:
            print(f"VALUE ERROR- {err}")

        except Exception as err:
            print(f"EXCEPTION- {err}")

    return feats
