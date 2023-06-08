import math

import matplotlib.pyplot as plt
import numpy as np

from ...plots import plot_image, save_image
from ...utils import (
    NumLst,
    PathType,
    PathTypeLst,
    StrLst,
    image_path_to_data_ax,
    path_in,
    save_path_file,
)


def images_path(
    paths: PathTypeLst,
    rows: int or None = None,
    columns: int or None = None,
    titles: StrLst = [],
    cmap: str or None = "gray",
    origin: str or None = "upper",
    save_path: PathType or None = None,
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
        origin=origin,
        save_path=save_path,
    )


def images_array(
    images_data: NumLst,
    rows=None,
    columns=None,
    titles=[],
    cmap="gray",
    origin="upper",
    save_path=None,
):
    print("Loading images...")

    if len(images_data) == 0:
        raise ValueError("images_data must be a list of arrays")

    for image_data in images_data:
        if image_data.ndim != 2:
            raise ValueError("Images must be 2D")

    num_images = len(images_data)  # Number of images
    rows = math.ceil(math.sqrt(num_images))  # Number of rows in the grid
    columns = math.ceil(num_images / rows)  # Number of columns in the grid

    _, axs = plt.subplots(rows, columns)
    if num_images == 1:
        axs = np.array([axs])

    for i, ax in enumerate(axs.flat):
        if i < num_images:
            title = titles[i] if titles else f"Image {i}"
            plot_image(ax, images_data[i], cmap=cmap, title=title, origin=origin)
            ax.axis("off")

        else:
            ax.axis("off")

    plt.tight_layout()

    if save_path:
        save_path = save_path_file(save_path, suffix=".png")
        save_image(plt, save_path)
    else:
        plt.show()

    plt.close()
