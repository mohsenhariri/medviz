from pathlib import Path

import pandas as pd

from ..utils import path_in, save_path_file


def match_image_masks(
    images_path: str or Path,
    masks_path: str or Path,
    image_extension: str or None = None,
    mask_extension: str or None = None,
    image_id_func=lambda x: x,
    mask_id_func=lambda x: x,
    save_path: str or Path = Path("./output/match_image_masks.csv"),
):
    df_dict = {"ID": [], "Image": [], "Mask": []}

    images_path = path_in(images_path, env=False)
    masks_path = path_in(masks_path, env=False)

    if mask_extension is None:
        extensions = set()

        for file_path in masks_path.rglob("*"):
            if file_path.is_file():
                file_extension = file_path.suffix.lower()
                extensions.add(file_extension)

        for extension in extensions:
            if extension in [".nii", ".nii.gz", ".dcm", ".npy"]:
                mask_extension = extension
                break

    if image_extension is None:
        extensions = set()

        for file_path in images_path.rglob("*"):
            if file_path.is_file():
                file_extension = file_path.suffix.lower()

                extensions.add(file_extension)

        for extension in extensions:
            if extension in [".nii", ".nii.gz", ".dcm", ".npy"]:
                image_extension = extension
                break

    image_paths = masks_path.glob(rf"**/*{image_extension}")
    mask_paths = masks_path.glob(rf"**/*{mask_extension}")

    images = {}
    for image_path in image_paths:
        id = int(image_id_func(image_path.stem))
        image_path = str(image_path)
        if id in images.keys():
            images[id].append(image_path)
        else:
            images[id] = [image_path]

    masks = {}
    for mask_path in mask_paths:
        id = int(mask_id_func(mask_path.stem))
        mask_path = str(mask_path)
        if id in masks.keys():
            masks[id].append(mask_path)
        else:
            masks[id] = [mask_path]

    # find unique ids
    unique_ids = set(images.keys()).intersection(set(masks.keys()))

    # find all ids
    all_ids = set(images.keys()).union(set(masks.keys()))

    for id in all_ids:
        df_dict["ID"].append(id)

        if id in images.keys():
            df_dict["Image"].append(images[id])
        else:
            df_dict["Image"].append(None)
        if id in masks.keys():
            df_dict["Mask"].append(masks[id])
        else:
            df_dict["Mask"].append(None)

    df = pd.DataFrame(df_dict, columns=df_dict.keys())

    save_path = save_path_file(save_path, suffix=".csv")

    df.to_csv(save_path, index=False)

    print(f"Number of unique ids: {len(unique_ids)}")
    print(f"Number of all ids: {len(all_ids)}")
