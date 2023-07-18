import multiprocessing
from pathlib import Path

import medviz as viz

base_path = Path("/home/mohsen/dataset/nii_version/Grp1_TI_nii_raw")
mask_paths = base_path.glob("*.nii")

output_path = Path("/media/ext/hdd5t/dataset/Grp1_TI_nii_resampled")


def resample_mask(mask_path):
    print(f"Resampling {mask_path.name}...")
    mask_resampled_path = output_path / mask_path.name
    viz.resample(
        input_path=mask_path, output_path=mask_resampled_path, new_voxel_size=[1, 1, 1], method="nearest"
    )


def main():
    num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(resample_mask, mask_paths)


if __name__ == "__main__":
    main()
