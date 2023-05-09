import secrets

import nibabel as nib
import numpy as np


def assert_shape(arr: list) -> tuple:
    """
    Asserts that all segments have the same shape as the image
    :param arr: list of np arrays
    :return: tuple of the middle slice and the last slice
    usage:
        init_slice, last_slice = assert_shape(ct_data + masks_data)
    """
    # arr[0] is the image
    # arr[1:] are the segments
    # m,n,d are the dimensions of the image
    n, m, d = arr[0].shape
    try:
        for np_array in arr:
            assert np_array.shape == (m, n, d)
    except AssertionError:
        raise ValueError("All segments must have the same shape as the image")

    return d // 2, d - 1


def generate_mask_colors(num_masks, mask_colors=None):
    if mask_colors is None:
        mask_colors = ["#" + secrets.token_hex(3) for _ in range(num_masks)]

        return mask_colors
    else:
        try:
            assert num_masks == len(mask_colors)
            return mask_colors
        except AssertionError:
            raise ValueError(
                f"Number of masks ({num_masks}) does not match number of colors ({len(mask_colors)})"
            )


def mask_path_to_data(mask_path):
    mask = nib.load(mask_path)
    mask_data = mask.get_fdata()
    mask_data_bool = mask_data.astype(np.bool_)
    mask_data_bool_rot = np.flip(np.rot90(mask_data_bool, axes=(1, 0)), axis=1)
    # mask_data = np.ma.masked_where(mask_data == False, mask_data)
    return mask_data_bool_rot


def image_path_to_data(mask_path):
    image = nib.load(mask_path)
    image_data = image.get_fdata()
    image_data_rot = np.flip(np.rot90(image_data, axes=(1, 0)), axis=1)
    return image_data_rot


def plot_image(ax, image_data, cmap="gray"):
    ax.imshow(image_data, cmap=cmap)


def plot_mask_neighbor(ax, mask_data, cmap="jet", alpha=0.3):
    # ax.imshow(mask_data, cmap=cmap, alpha=alpha, interpolation="bilinear", vmin=0, vmax=1)
    ax.imshow(mask_data, cmap=cmap, alpha=alpha)


# def plot_contour(ax, mask_data, color, line_width=0.5,levels=[0.5]):
#     ax.contour(mask_data, colors=color, linewidths=line_width,levels=levels)
# ax.contour(mask_data, colors=color, linewidths=line_width, levels=[0.5], alpha=0.5)


def plot_contour(ax, mask_data, color, levels=[0.5]):
    ax.contour(mask_data, colors=color, levels=levels)
