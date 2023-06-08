import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

from ...plots import generate_mask_colors, plot_contour
from ...utils import NumLst, PathTypeLst, StrLst, mask_path_to_data_ax, path_in


def masks_path(
    paths: PathTypeLst,
    rows: int or None = None,
    columns: int or None = None,
    titles: StrLst = [],
    mask_colors=None,
    origin="upper",
):
    if len(paths) == 0:
        raise ValueError("paths must be a list of paths")

    paths = [path_in(path) for path in paths]

    masks_data = [mask_path_to_data_ax(path) for path in paths]

    masks_array(
        masks_data=masks_data,
        rows=rows,
        columns=columns,
        titles=titles,
        mask_colors=mask_colors,
        origin=origin,
    )


def masks_array(
    masks_data: NumLst,
    rows=None,
    columns=None,
    titles=[],
    mask_colors=[],
    origin="upper",
):
    print("Loading images...")

    if len(masks_data) == 0:
        raise ValueError("images_data must be a list of arrays")

    for mask_data in masks_data:
        if mask_data.ndim != 3:
            raise ValueError("images_data must be a list of 3D arrays")

    num_masks = len(masks_data)  # Number of images

    if rows is None and columns is None:
        rows = math.ceil(math.sqrt(num_masks))  # Number of rows in the grid
        columns = math.ceil(num_masks / rows)  # Number of columns in the grid
    elif rows is None:
        rows = math.ceil(num_masks / columns)
    elif columns is None:
        columns = math.ceil(num_masks / rows)

    if num_masks > rows * columns:
        raise ValueError("rows * columns must be greater than or equal to num_images")

    depth = [mask_data.shape[2] for mask_data in masks_data]

    init_slice, last_slice = int(np.mean(depth) // 2), np.max(depth) - 2

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    _, axs = plt.subplots(rows, columns)
    if num_masks == 1:
        axs = np.array([axs])

    plt.subplots_adjust(bottom=0.25)

    for i, ax in enumerate(axs.flat):
        if i < num_masks:
            title = titles[i] if titles else f"Image {i}"

            plot_contour(
                ax,
                masks_data[i][:, :, init_slice],
                color=mask_colors[i],
                title=title,
                origin=origin,
                levels=[0.5],
            )
            # ax.axis("off")
            ax.set_xlabel(f"Slice Number: {init_slice}")

        else:
            ax.axis("off")

    slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])

    slider = Slider(
        slider_ax,
        "Slice",
        0,
        last_slice,
        valinit=init_slice,
        valstep=1,
    )

    def update(val):
        slice_num = int(slider.val)

        for i, ax in enumerate(axs.flat):
            ax.clear()

            if i < num_masks:
                title = titles[i] if titles else f"Image {i}"

                if masks_data[i].shape[2] <= slice_num:
                    slice_num = masks_data[i].shape[2] - 1

                plot_contour(
                    ax,
                    masks_data[i][:, :, slice_num],
                    color=mask_colors[i],
                    title=title,
                    origin=origin,
                    levels=[0.5],
                )
                ax.set_xlabel(f"Slice Number: {slice_num}")
                # ax.axis("off")
            else:
                ax.axis("off")
                pass
        # ax.set_title(title)

    slider.on_changed(update)

    plt.tight_layout()
    plt.show()
