from pathlib import Path

import pandas as pd

import medviz as viz


def generate_mask_schema(
    dataset_path,
    id_func=lambda x: x,
    mask_format=".nii",
    output_path=r"./",
    output_name="mask_schema.csv",
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

    mask_paths = dataset_path.glob(rf"**/*{mask_format}")

    for mask_path in mask_paths:
        # try:
        id = id_func(mask_path.stem)
        print(id)
        mask_characteristics = viz.get_characteristics(mask_path)
        most_value_nonzero_slices, num_nonzero_slices = viz.significant_slice_idx(
            mask_path
        )
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

    output_path = Path(output_path)
    if not output_path.exists():
        output_path.mkdir(parents=True)

    save_path = Path(output_path) / Path(output_name)
    df.to_csv(save_path, index=False)

    print("Done!")
