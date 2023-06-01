from pathlib import Path

import pandas as pd
import pydicom


def read_dicom_metadata(filepath):
    ds = pydicom.dcmread(filepath)
    metadata = {}

    for element in ds.iterall():
        if (
            element.VR != "SQ"
            and element.VR != "OB"
            and element.VR != "OW"
            and element.VR != "OF"
            and element.VR != "UN"
        ):
            metadata[element.keyword] = element.value

    return metadata


def save_dicom_metadata(base_path, id_func=lambda x: x, pattern="**/*.dcm", save_path: str or Path = "./"):
    paths = Path(base_path).glob(pattern)
    metadata_list = []

    for path in paths:
        id = id_func(path.stem)

        metadata = read_dicom_metadata(path)
        metadata["ID"] = id
        metadata["Path"] = str(path)
        metadata_list.append(metadata)

    df = pd.DataFrame(metadata_list)

    save_path = Path(save_path)
    if not save_path.exists():
        save_path.mkdir(parents=True)

    save_path = save_path / Path("metadata.csv")

    df.to_csv(save_path, index=False)
