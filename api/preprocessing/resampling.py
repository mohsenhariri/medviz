from pathlib import Path

import medviz as viz

mask_path = Path("dataset/1-1-label.nii")
mask_resampled_path = Path("dataset/resampled/1-1-label.nii")

image_path = Path("dataset/1-1.nii")
image_resampled_path = Path("dataset/resampled/1-1_resampled.nii")

viz.resample(
    input_path=mask_path,
    output_path=mask_resampled_path,
    new_voxel_size=[1, 1, 1],
    method="nearest",
)

viz.resample(
    input_path=image_path,
    output_path=image_resampled_path,
    new_voxel_size=[1, 1, 1],
    method="trilinear",
)
