import nibabel as nib
import numpy as np


def get_characteristics(mask_path) -> dict:
    """
    This function takes in a path to a mask and returns a dictionary of characteristics of the mask.
    The characteristics are:
    - shape: the shape of the mask
    - data_type: the data type of the mask
    - values: the unique values in the mask and their counts
    - mask_type: the type of mask (empty, binary, or multi-class)
    :param mask_path: path to the mask
    :return: a dictionary of characteristics of the mask
    """

    nib_mask = nib.load(mask_path)
    mask = nib_mask.get_fdata()
    shape = mask.shape
    data_type = mask.dtype

    unique, counts = np.unique(mask, return_counts=True)
    values = dict(zip(unique, counts))

    if len(unique) == 1:
        mask_type = "Empty"
    elif len(unique) == 2:
        mask_type = "Binary"
    else:
        mask_type = "Multi-class"

    mask_characteristics = {
        "shape": shape,
        "data_type": data_type,
        "values": values,
        "mask_type": mask_type,
    }
    return mask_characteristics


def significant_slice_idx(mask_path) -> tuple:
    """
    This function takes in a path to a mask and returns the most significant slice index and the number of nonzero slices.
    The most significant slice is the slice with the most nonzero pixels.
    The number of nonzero slices is the number of slices with at least one nonzero pixel.
    :param mask_path: path to the mask
    :return: a tuple of the most significant slice index and the number of nonzero slices
    """

    if get_characteristics(mask_path)["mask_type"] != "Binary":
        raise ValueError("The mask must be binary.")

    mask_nb = nib.load(mask_path)
    mask = mask_nb.get_fdata()
    mask_bool = mask.astype(np.bool_)

    most_value_nonzero_slices, num_nonzero_slices = significant_slice_idx_data(
        mask_bool
    )

    return most_value_nonzero_slices, num_nonzero_slices


def significant_slice_idx_data(mask_bool) -> tuple:
    """_summary_

    Args:
        mask_bool (_type_): _description_

    Returns:
        tuple: _description_
    """
    z_sum = np.sum(mask_bool, axis=(0, 1))

    most_value_slices = np.argsort(z_sum)[::-1]

    num_nonzero_slices = np.count_nonzero(z_sum)

    most_value_nonzero_slices = most_value_slices[:num_nonzero_slices]

    return most_value_nonzero_slices, num_nonzero_slices


def mask_path_to_data_ax(mask_path):
    mask = nib.load(mask_path)
    mask_data = mask.get_fdata()

    mask_data_bool = mask_data.astype(np.bool_)
    mask_data_bool_rot = np.flip(np.rot90(mask_data_bool, axes=(1, 0)), axis=1)
    # mask_data = np.ma.masked_where(mask_data == False, mask_data)
    return mask_data_bool_rot


def mask_path_to_data_sag(mask_path):
    mask = nib.load(mask_path)
    mask_data = mask.get_fdata()

    mask_data_bool = mask_data.astype(np.bool_)
    mask_data_bool_rot = np.flip(np.rot90(mask_data_bool, axes=(1, 2)), axis=1)
    # mask_data = np.ma.masked_where(mask_data == False, mask_data)
    return mask_data_bool_rot


def image_path_to_data_ax(mask_path):
    image = nib.load(mask_path)
    image_data = image.get_fdata()
    image_data_rot = np.flip(np.rot90(image_data, axes=(1, 0)), axis=1)
    return image_data_rot


def image_path_to_data_sag(mask_path):
    image = nib.load(mask_path)
    image_data = image.get_fdata()

    image_data_rot = np.flip(np.rot90(image_data, axes=(1, 2)), axis=1)
    return image_data_rot


def expand(mask_path, expand_factor=5):
    mask_data = mask_path_to_data_ax(mask_path)

    most_value_nonzero_slices, _ = significant_slice_idx_data(mask_data)

    for d in most_value_nonzero_slices:
        arr = mask_data[:, :, d]
        indices = np.argwhere(arr)
        for m, n in indices:
            blowup_factor = expand_factor
            for i in range(-blowup_factor, blowup_factor + 1):
                for j in range(-blowup_factor, blowup_factor + 1):
                    mask_data[m + i, n + j, d] = True

    return mask_data


def mask_expand(mask_expert_path, mask_paths, expand_factor=5):
    mask_expert_data = expand(mask_expert_path, expand_factor=expand_factor)

    masks_data = []
    for mask_path in mask_paths:
        mask_data = mask_path_to_data_ax(mask_path)
        mask_data = mask_data * mask_expert_data

        masks_data.append(mask_data)

    return mask_expert_data, masks_data
