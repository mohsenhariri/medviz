from pathlib import Path

import pandas as pd


def match_image_mask(
    images_path, masks_path, image_func, mask_func, pattern: str, save_path="./"
):
    df_dict = {"ID": [], "Image": [], "Mask": []}

    image_paths = Path(images_path).glob(pattern)
    mask_paths = Path(masks_path).glob(pattern)

    images = {}
    for image_path in image_paths:
        id = int(image_func(image_path.stem))
        image_path = str(image_path)
        if id in images.keys():
            images[id].append(image_path)
        else:
            images[id] = [image_path]

    masks = {}
    for mask_path in mask_paths:
        id = int(mask_func(mask_path.stem))
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
    save_path = Path(save_path)
    if not save_path.exists():
        save_path.mkdir(parents=True)

    save_path = save_path / Path("image_mask.csv")
    df.to_csv(save_path, index=False)

    print(f"Number of unique ids: {len(unique_ids)}")
    print(f"Number of all ids: {len(all_ids)}")
