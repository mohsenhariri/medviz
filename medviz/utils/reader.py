"""
Medical image reader

Extensions:
    - DICOM
    - NIFTI
    - MHA
    
"""
from pathlib import Path

import nibabel as nib
import numpy as np
import pydicom as dicom
import SimpleITK as sitk

from .custom_type import PathType
from .helper_path import path_in


def reader(
    path: PathType,
) -> nib.Nifti1Image or dicom.dataset.FileDataset or sitk.Image:
    """
    Read the medical image based on its file extension.

    Parameters:
        path (Union[str, Path]): Path to the image.

    Returns:
        Loaded image object.
    """
    path = path_in(path)
    if path.suffix in [".nii", ".nii.gz"]:
        return nib.load(path)
    elif path.suffix == ".dcm":
        return dicom.dcmread(path)
    elif path.suffix == ".mha":
        return sitk.ReadImage(str(path))
    else:
        raise TypeError(f"Unsupported file type: {path.suffix}")


def im2arr(path: str or Path) -> np.ndarray:
    """
    Convert the medical image to a numpy array based on its file extension.

    Parameters:
        path (Union[str, Path]): Path to the image.

    Returns:
        Image data as a numpy array.
    """
    path = path_in(path)
    if path.suffix in [".nii", ".nii.gz"]:
        return nib.load(path).get_fdata()
    elif path.suffix == ".dcm":
        return dicom.dcmread(path).pixel_array
    elif path.suffix == ".mha":
        sitk_image = sitk.ReadImage(
            str(path)
        )  # SimpleITK python wrapper has no support for pathlib.Path
        return sitk.GetArrayFromImage(sitk_image)
    else:
        raise TypeError(f"Unsupported file type: {path.suffix}")
