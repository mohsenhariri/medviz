## `resample` Function

The `resample` function is designed to resample a medical image to a specified voxel size using a given interpolation method. Resampling is often required in medical imaging to ensure that datasets have a consistent spatial resolution, which can be crucial for certain analyses or algorithms.

### Arguments

- **`path` (PathType)**: 
  - **Description**: The path to the input image that you want to resample.
  - **Example**: `"./data/patient1_scan.nii.gz"`

- **`voxel_size` (List[float], default=[1.0, 1.0, 1.0])**: 
  - **Description**: The desired output voxel size. It defines the spacing between pixels/voxels in each dimension.
  - **Example**: `[0.5, 0.5, 0.5]` would specify a half-millimeter cubic voxel size.

- **`method` (str, default="trilinear")**: 
  - **Description**: Specifies the interpolation method used during resampling.
    - `"nearest"`: Nearest neighbor interpolation. Useful for categorical or label images.
    - `"trilinear"`: Linear interpolation in 3D. Generally used for standard image data.
  - **Example**: `"nearest"`

- **`out_path` (Optional[PathType], default=None)**:
  - **Description**: The directory path where the resampled image will be saved. If not provided, the function defaults to the directory of the input image.
  - **Example**: `"./output"`

- **`file_name` (Optional[str], default=None)**:
  - **Description**: Name for the output resampled file. If not provided, the function will append `"_resampled_{method}"` to the original filename.
  - **Example**: `"patient1_resampled.nii.gz"`

### Returns

- **sitk.Image**: The resampled image in the SimpleITK format.

### Usage Example

Suppose you have an image stored at `"./data/patient1_scan.nii.gz"` and you want to resample it to a voxel size of `[0.5, 0.5, 0.5]` using nearest neighbor interpolation. You can call the function like:

```python
resampled_img = viz.resample("./data/patient1_scan.nii.gz", voxel_size=[0.1, 0.1, 0.1], method="nearest")
```

The resampled image will be saved to `"./data/patient1_scan_resampled_nearest.nii.gz"`.


```python
resampled_img = resample("./data/patient1_scan.nii.gz", voxel_size=[0.5, 0.5, 0.5], method="nearest", out_path="./output", file_name="patient1_resampled.nii.gz")
```

The resampled image will be saved to `"./output/patient1_resampled.nii.gz"`.


