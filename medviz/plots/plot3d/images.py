import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

from ...plots import plot_image
from ...utils import NumLst, PathTypeLst, StrLst, image_path_to_data_ax, path_in


def images_path(
    paths: PathTypeLst,
    rows: int or None = None,
    columns: int or None = None,
    titles: StrLst = [],
    cmap: str or None = "gray",
):
    if len(paths) == 0:
        raise ValueError("paths must be a list of paths")

    paths = [path_in(path) for path in paths]

    images_data = [image_path_to_data_ax(path) for path in paths]

    images_array(
        images_data=images_data,
        rows=rows,
        columns=columns,
        titles=titles,
        cmap=cmap,
    )


def images_array(
    images_data: NumLst,
    rows=None,
    columns=None,
    titles=[],
    cmap="gray",
):
    print("Loading images...")

    if len(images_data) == 0:
        raise ValueError("images_data must be a list of arrays")

    for image_data in images_data:
        if image_data.ndim != 3:
            raise ValueError("images_data must be a list of 3D arrays")

    num_images = len(images_data)  # Number of images

    if rows is None and columns is None:
        rows = math.ceil(math.sqrt(num_images))  # Number of rows in the grid
        columns = math.ceil(num_images / rows)  # Number of columns in the grid
    elif rows is None:
        rows = math.ceil(num_images / columns)
    elif columns is None:
        columns = math.ceil(num_images / rows)

    if num_images > rows * columns:
        raise ValueError("rows * columns must be greater than or equal to num_images")

    depth = [image_data.shape[2] for image_data in images_data]

    init_slice, last_slice = int(np.mean(depth) // 2), np.max(depth) - 2

    _, axs = plt.subplots(rows, columns)
    if num_images == 1:
        axs = np.array([axs])

    plt.subplots_adjust(bottom=0.25)

    for i, ax in enumerate(axs.flat):
        if i < num_images:
            title = titles[i] if titles else f"Image {i}"
            plot_image(ax, images_data[i][:, :, init_slice], cmap=cmap, title=title)
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

            if i < num_images:
                title = titles[i] if titles else f"Image {i}"

                if images_data[i].shape[2] <= slice_num:
                    slice_num = images_data[i].shape[2] - 1
                plot_image(ax, images_data[i][:, :, slice_num], cmap=cmap, title=title)
                ax.set_xlabel(f"Slice Number: {slice_num}")
                # ax.axis("off")
            else:
                ax.axis("off")
                pass
        # ax.set_title(title)

    slider.on_changed(update)

    plt.tight_layout()
    plt.show()
