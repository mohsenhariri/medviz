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


def im2arr(path: PathType) -> np.ndarray:
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
    elif path.suffix == ".npy":
        return np.load(path)
    else:
        raise TypeError(f"Unsupported file type: {path.suffix}")


def image_preprocess(input):
    if isinstance(input, PathType):
        data = im2arr(input)
    elif isinstance(input, np.ndarray):
        data = input
    else:
        raise ValueError(
            "Unsupported input type. Expected path (str or Path) or numpy ndarray."
        )

    data = data.astype(np.float64)
    min_value = np.min(data)
    max_value = np.max(data)
    data = (data - min_value) / (max_value - min_value)

    return data


def mask_preprocess(input):
    if isinstance(input, PathType):
        data = im2arr(input)
    elif isinstance(input, np.ndarray):
        data = input
    else:
        raise ValueError(
            "Unsupported input type. Expected path (str or Path) or numpy ndarray."
        )

    data = data.astype(np.int8)

    return data


def read_image_mask(image, mask) -> np.ndarray:
    """
    Read the medical image and mask based on their file extension.

    Parameters:
        image (Union[str, Path] or np.ndarray): Path to the image or image data.
        mask (Union[str, Path] or np.ndarray): Path to the mask or mask data.

    Returns:
        Loaded image and mask as numpy arrays.
    """

    image = image_preprocess(image)
    mask = mask_preprocess(mask)

    assert image.shape == mask.shape, "Image and mask shape mismatch"

    print("Image shape", image.shape)
    print("Mask shape", mask.shape)

    return image, mask
