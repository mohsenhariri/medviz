from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from tabulate import tabulate

from ..utils import path2loader, path_in, save_path_file
from .meta_helpers import _metadata_nibabel, _metadata_pydicom, _metadata_sitk


def metadata(
    image_paths: Union[List[Union[str, Path]], Union[str, Path]],
    save_csv: Optional[Union[str, Path]] = None,
) -> List[Dict[str, Any]]:
    """
    Extracts and optionally saves metadata from one or more NIFTI images.

    Parameters:
        image_paths: Union[List[Union[str, Path]], Union[str, Path]] - The paths to the NIFTI images.
        save_csv: Optional[Union[str, Path]] - The path where to save the metadata as a CSV file.

    Returns:
        A list of dictionaries, each containing the metadata for one image.
    """

    if not isinstance(image_paths, list):
        image_paths = [image_paths]

    all_image_info = []

    for image_path in image_paths:
        image_path = path_in(image_path)
        # image_info: Dict[str, Any] = {}

        # try:
        #     image = nib.load(image_path)
        # except nib.filebasedimages.ImageFileError:
        #     print(f"Error: {image_path} is not a valid NIFTI image.")
        #     continue

        try:
            image_and_properties, reader, image_and_properties_itk = path2loader(
                image_path
            )

        except Exception as e:
            print("Error reading image", e)

            raise e

        merged_dict = {
            "name": image_path.name,
            **_metadata_sitk(image_and_properties_itk),
        }

        if reader == "nibabel":
            metadata_nib = _metadata_nibabel(image_and_properties)
            merged_dict = {**merged_dict, **metadata_nib}

        elif reader == "pydicom":
            metadata_dicom = _metadata_pydicom(image_and_properties)
            merged_dict = {**merged_dict, **metadata_dicom}

        all_image_info.append(merged_dict)

    if save_csv:
        csv_path = save_path_file(save_csv, suffix=".csv")
        df = pd.DataFrame(all_image_info)
        df.to_csv(csv_path, index=False)

    else:
        for info in all_image_info:
            print(tabulate(info.items(), tablefmt="fancy_grid"))

    return all_image_info
