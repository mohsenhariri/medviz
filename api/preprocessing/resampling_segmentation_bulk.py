from pathlib import Path

from tqdm import tqdm

import medviz as viz

base_path = Path("dataset/nii_version/Grp1_TI_nii_raw")
mask_paths = base_path.glob("*.nii")

output_path = Path("/nii_version/Grp1_TI_nii_resampled")

mask_paths = list(mask_paths)
num_inputs = len(mask_paths)

for mask_path in tqdm(mask_paths, total=num_inputs, desc="Progress"):
    print(f"Resampling {mask_path.name}...")
    mask_resampled_path = output_path / mask_path.name
    viz.resample(
        path=mask_path,
        out_path=mask_resampled_path,
        voxel_size=[1, 1, 1],
        method="nearest",
    )
