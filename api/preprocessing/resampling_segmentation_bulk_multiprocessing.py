import multiprocessing
from pathlib import Path

import medviz as viz

base_path = Path("Input Data Path")
mask_paths = base_path.glob("*.mha")

output_path = Path("Input Output Path")


def resample_mask(mask_path):
    print(f"Resampling {mask_path.name}...")
    mask_resampled_path = output_path / mask_path.name
    viz.resample(
        path=mask_path,
        out_path=mask_resampled_path,
        voxel_size=[1, 1, 1],
        method="nearest",
    )


def main():
    num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(resample_mask, mask_paths)


if __name__ == "__main__":
    main()
