"""
Medical image reader

Extensions:
    - DICOM
    - NIFTI
    - MHA
    
"""

from pathlib import Path
from typing import Tuple, Union

import nibabel as nib
import numpy as np
import pydicom as dicom
import SimpleITK as sitk

from .custom_type import MedicalImage, PathMedicalImage, PathNpType
from .helper_path import path_in


def path2loader(path: PathMedicalImage) -> PathMedicalImage:
    if isinstance(path, MedicalImage):
        return path

    path_obj = path_in(path)
    suffixes = path_obj.suffixes

    try:
        if suffixes[-2:] == [".nii", ".gz"] or suffixes[-1:] == [".nii"]:
            image_and_properties = nib.load(path)
            reader = "nibabel"

        elif suffixes[-1:] == [".dcm"]:
            image_and_properties = dicom.dcmread(path)
            reader = "pydicom"
        else:
            image_and_properties = None
            reader = None

        image_and_properties_itk = sitk.ReadImage(str(path))

    except Exception as e:
        print("Error reading image", e)
        raise e

    return (image_and_properties, reader, image_and_properties_itk)


def im2arr(*paths: PathNpType) -> Union[np.ndarray, Tuple[np.ndarray]]:
    """
    Convert one or more medical images to numpy arrays based on their file extensions.

    Parameters:
        *paths (Union[str, Path]): Paths to the medical image files or already loaded numpy arrays.

    Returns:
        Union[np.ndarray, Tuple[np.ndarray]]: If a single path is provided, returns the image data as a numpy array.
                                             If multiple paths are provided, returns a tuple of numpy arrays.

    Raises:
        TypeError: If the provided file format is unsupported.
    """

    def load_image_as_array(path: Union[str, Path]) -> np.ndarray:
        if isinstance(path, np.ndarray):
            return path

        path_obj = Path(path)
        suffixes = path_obj.suffixes

        if suffixes[-2:] == [".nii", ".gz"] or suffixes[-1:] == [".nii"]:
            return nib.load(path_obj).get_fdata()

        elif suffixes[-1:] == [".dcm"]:
            return dicom.dcmread(path_obj).pixel_array

        elif suffixes[-1:] == [".mha"]:
            sitk_image = sitk.ReadImage(
                str(path_obj)
            )  # SimpleITK python wrapper has no support for pathlib.Path
            return sitk.GetArrayFromImage(sitk_image)
        elif suffixes[-1:] == [".npy"]:
            return np.load(path_obj)
        elif suffixes[-1:] == [".npz"]:
            return np.load(path_obj)["arr_0"]
        else:
            raise TypeError(f"Unsupported file type: {path_obj.suffix}")

    arrays = tuple(load_image_as_array(path) for path in paths)
    if len(arrays) == 1:
        return arrays[0]
    return arrays


def image_preprocess(input, norm: bool) -> np.ndarray:
    """
    Preprocesses the given image by converting it into an array, optionally normalizing it.

    Parameters:
    - input (Union[str, np.ndarray, Any]): The input image to preprocess. This can be a path to the image file,
      an image in numpy array format, or any other format supported by the im2arr function.
    - norm (bool): If set to True, the data will be normalized to fall between 0 and 1.

    Returns:
    - np.ndarray: The preprocessed image in numpy array format.

    Note:
    The function assumes that the im2arr function can convert the provided input into a numpy array.
    """

    data = im2arr(input)
    data = data.astype(np.float64)

    if norm:
        min_value = np.min(data)
        max_value = np.max(data)
        data = (data - min_value) / (max_value - min_value)

    return data


def mask_preprocess(input) -> np.ndarray:
    """
    Preprocesses the given mask by converting it into an array and setting its datatype to int8.

    Parameters:
    - input (Union[str, np.ndarray, Any]): The input mask to preprocess. This can be a path to the mask file,
      a mask in numpy array format, or any other format supported by the im2arr function.

    Returns:
    - np.ndarray: The preprocessed mask in numpy array format.

    Note:
    The function assumes that the im2arr function can convert the provided input into a numpy array.
    """

    data = im2arr(input)
    data = data.astype(np.int8)

    return data


def read_image_mask(
    image: Union[str, Path, np.ndarray],
    mask: Union[str, Path, np.ndarray],
    norm: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Reads the medical image and its corresponding mask, ensuring they both have
    the same shape after preprocessing. If a normalization flag is set for the
    image, it will normalize the image data to [0, 1].

    Parameters:
    - image (Union[str, Path, np.ndarray]): Either a path to the medical image
      file (supporting the formats as defined in image_preprocess function) or
      an already loaded numpy array of the image data.
    - mask (Union[str, Path, np.ndarray]): Similarly, either a path to the mask
      file or an already loaded numpy array of the mask.
    - norm (bool, optional): A flag to decide whether to normalize the image data
      to range [0, 1]. Defaults to False.

    Returns:
    - Tuple[np.ndarray, np.ndarray]: A tuple containing the processed image and
      mask as numpy arrays.

    Raises:
    - ValueError: If the processed image and mask have different shapes.

    Note:
    Ensure that the image_preprocess and mask_preprocess functions are
    properly defined and compatible with the inputs you expect for this function.
    """

    image = image_preprocess(image, norm)
    mask = mask_preprocess(mask)

    if image.shape != mask.shape:
        raise ValueError("Image and mask shape mismatch")

    return image, mask
