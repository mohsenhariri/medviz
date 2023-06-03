from pathlib import Path

import pandas as pd

from ..utils import get_characteristics, path_in, save_path_file, significant_slice_idx


def generate_mask_schema(
    masks_path: str or Path,
    id_func=lambda x: x,
    mask_extension=None,
    save_path: str or Path = Path("./output/mask_profile.csv"),
):
    df_dict = {
        "id": [],
        "path": [],
        "shape": [],
        "data_type": [],
        "values": [],
        "mask_type": [],
        "most_value_nonzero_slices": [],
        "num_nonzero_slices": [],
    }

    dataset_path = path_in(masks_path, env=False)

    if mask_extension is None:
        extensions = set()

        for file_path in dataset_path.rglob("*"):
            if file_path.is_file():
                file_extension = file_path.suffix.lower()

                extensions.add(file_extension)

        for extension in extensions:
            if extension in [".nii", ".nii.gz", ".dcm"]:
                mask_extension = extension
                break

    mask_paths = dataset_path.glob(rf"**/*{mask_extension}")

    for mask_path in mask_paths:
        # try:
        id = id_func(mask_path.stem)
        print(id)
        mask_characteristics = get_characteristics(mask_path)
        most_value_nonzero_slices, num_nonzero_slices = significant_slice_idx(mask_path)
        df_dict["id"].append(id)
        df_dict["path"].append(Path(*mask_path.parts[-3:]))
        df_dict["shape"].append(mask_characteristics["shape"])
        df_dict["data_type"].append(mask_characteristics["data_type"])
        df_dict["values"].append(mask_characteristics["values"])
        df_dict["mask_type"].append(mask_characteristics["mask_type"])
        df_dict["most_value_nonzero_slices"].append(most_value_nonzero_slices)
        df_dict["num_nonzero_slices"].append(num_nonzero_slices)

    # except Exception as e:
    #     print(f"Error in {mask_path}", e)

    df = pd.DataFrame(df_dict, columns=df_dict.keys())

    save_path = save_path_file(save_path, suffix=".csv")

    df.to_csv(save_path, index=False)

    print("Done!")
