from typing import Optional

import numpy as np
import SimpleITK as sitk

from ..utils import PathType, path_in, save_path_file


def resample(
    path: PathType,
    voxel_size: list = [1.0, 1.0, 1.0],
    method: str = "trilinear",
    out_path: Optional[PathType] = None,
    file_name: Optional[str] = None,
):
    path = path_in(path)
    itk_image = sitk.ReadImage(path)

    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()
    print(f"original_size: {original_size}")
    print(f"original_spacing: {original_spacing}")

    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / voxel_size[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / voxel_size[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / voxel_size[2]))),
    ]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(voxel_size)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if method == "nearest":
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    elif method == "trilinear":
        resample.SetInterpolator(sitk.sitkLinear)
    else:
        raise ValueError("Unknown interpolation method")

    resampled_image = resample.Execute(itk_image)

    print(f"resampled_size: {resampled_image.GetSize()}")
    print(f"resampled_spacing: {resampled_image.GetSpacing()}")

    if not out_path:
        out_path = path.parent

    if not file_name:
        file_name = path.stem + f"_resampled_{method}" + path.suffix

    full_path = save_path_file(out_path / file_name, path.suffix)
    sitk.WriteImage(resampled_image, str(full_path))
    print(f"Saved to {full_path}")

    return resampled_image
