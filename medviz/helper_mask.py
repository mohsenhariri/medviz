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
