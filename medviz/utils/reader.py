"""
Medical image reader

Extensions:
    - DICOM
    - NIFTI

"""
from pathlib import Path

import nibabel as nib
import numpy as np
import pydicom as dicom

from .helper_path import path_in


def reader(path: str or Path) -> nib.Nifti1Image or dicom.dataset.FileDataset:
    path = path_in(path)
    if path.suffix == ".nii" or path.suffix == ".nii.gz":
        return nib.load(path)
    elif path.suffix == ".dcm":
        return dicom.dcmread(path)
    else:
        raise TypeError(f"Unsupported file type: {path.suffix}")


def convert_arr(path: str or Path) -> np.ndarray:
    path = path_in(path)
    if path.suffix == ".nii" or path.suffix == ".nii.gz":
        return nib.load(path).get_fdata()
    elif path.suffix == ".dcm":
        return dicom.dcmread(path).pixel_array
    else:
        raise TypeError(f"Unsupported file type: {path.suffix}")
