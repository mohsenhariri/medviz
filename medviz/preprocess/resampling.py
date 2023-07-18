import nibabel as nib
import numpy as np

from ..utils import path_in, save_path_file


def resample(input_path, output_path, new_voxel_size, method="nearest"):
    input_path = path_in(input_path)

    # Load the input NIfTI image
    img = nib.load(input_path)
    data = img.get_fdata()
    affine = img.affine

    header = img.header
    voxel_dims = header.get_zooms()[:3]
    current_voxel_size = voxel_dims

    print("Current voxel size", current_voxel_size)
    current_voxel_size = np.array(current_voxel_size)

    scaling_factors = current_voxel_size / new_voxel_size
    print("Scaling factors", scaling_factors)

    # Compute the new shape after resampling
    print("Input shape", data.shape)
    new_shape = np.ceil(data.shape * scaling_factors).astype(int)
    print("Output shape", new_shape)

    resampled_data = np.zeros(new_shape, dtype=data.dtype)

    # Iterate over each voxel in the resampled image
    for i in range(new_shape[0]):
        for j in range(new_shape[1]):
            for k in range(new_shape[2]):
                # Compute the corresponding voxel indices in the original image
                orig_i = int(i / scaling_factors[0])
                orig_j = int(j / scaling_factors[1])
                orig_k = int(k / scaling_factors[2])

                if (
                    0 <= orig_i < data.shape[0]
                    and 0 <= orig_j < data.shape[1]
                    and 0 <= orig_k < data.shape[2]
                ):
                    resampled_data[i, j, k] = data[orig_i, orig_j, orig_k]

    # Create a new NIfTI image with resampled data and the same affine
    resampled_img = nib.Nifti1Image(resampled_data, affine)

    # Save the resampled image to the output path
    save_path = save_path_file(output_path, suffix=".nii")

    nib.save(resampled_img, save_path)
