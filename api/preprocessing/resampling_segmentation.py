from pathlib import Path

import medviz as viz

mask_path = Path("dataset/80-1-label.nii")
mask_resampled_path = Path("dataset/80-1-label_resampled.nii")

viz.resample(
    input_path=mask_path, output_path=mask_resampled_path, new_voxel_size=[1, 1, 1], method="nearest"
)
