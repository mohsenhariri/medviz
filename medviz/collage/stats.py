import ast
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd

from medviz.utils.helper_path import save_path_dir

from .compute_collage import compute_collage


def compute_stats_collage(
    csv_path: Path or str, stats_save_path: Path or str, base_path=None, raw_save_path: Path or str = None
):
    stats_save_path = save_path_dir(stats_save_path)
    raw_save_path = save_path_dir(raw_save_path) if raw_save_path else None

    df = pd.read_csv(csv_path)
    for idx, row in df.iterrows():
        print(f"Processing {row['ID']} ...")

        path_image = ast.literal_eval(row["Image"])
        path_masks = ast.literal_eval(row["Mask"])

        path_image = Path(path_image[0])
        path_image = path_image if base_path is None else base_path / path_image

        for path_mask in path_masks:
            try:
                path_mask = Path(path_mask)
                path_mask = path_mask if base_path is None else base_path / path_mask
                mask_name = Path(path_mask).stem

                extension = path_mask.suffix

                if extension == ".npy":
                    mask = np.load(path_mask)
                    image = np.load(path_image)
                elif extension in [".nii", ".nii.gz"]:
                    image = nib.load(path_image).get_fdata()
                    mask = nib.load(path_mask).get_fdata()
                else:
                    raise ValueError("Unknown extension")

                image = np.swapaxes(image, 0, 2)
                mask = np.swapaxes(mask, 0, 2)

                feats = compute_collage(
                    image,
                    mask,
                    haralick_windows=[3, 5, 7, 9, 11],
                    raw_save_path=raw_save_path,
                    name=mask_name,
                )

                stats_save_file = stats_save_path / f"{idx}_{mask_name}.npy"

                np.save(stats_save_file, feats)

            except FileNotFoundError as e:
                print("File not found:", e)

            except Exception as e:
                print("Exception occurred:", e)
