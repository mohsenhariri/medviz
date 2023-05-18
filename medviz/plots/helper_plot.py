import secrets
from pathlib import Path


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


def plot_image(ax, image_data, cmap="gray"):
    ax.imshow(image_data, cmap=cmap)


def plot_image_imshow(ax, arr, cmap="gray", origin="lower", title="", RGB=False):
    # ax.imshow(arr, cmap=cmap, origin=origin)
    ax.imshow(arr, cmap=cmap)

    ax.set_title(title)


def plot_mask_neighbor(ax, mask_data, cmap="jet", alpha=0.3):
    # ax.imshow(mask_data, cmap=cmap, alpha=alpha, interpolation="bilinear", vmin=0, vmax=1)
    ax.imshow(mask_data, cmap=cmap, alpha=alpha)


# def plot_contour(ax, mask_data, color, line_width=0.5,levels=[0.5]):
#     ax.contour(mask_data, colors=color, linewidths=line_width,levels=levels)
# ax.contour(mask_data, colors=color, linewidths=line_width, levels=[0.5], alpha=0.5)


def plot_contour(ax, mask_data, color, levels=[0.5]):
    ax.contour(mask_data, colors=color, levels=levels)


def save_image(plt, save_path):
    if isinstance(save_path, str):
        save_path = Path(save_path)

    if save_path.suffix != ".png":
        save_path = save_path.with_suffix(".png")

    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True)

    plt.savefig(save_path)
