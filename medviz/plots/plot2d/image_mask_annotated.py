"""
INPUT: 3D image, 3D mask
Finds slices with the most values 

OUTPU: 2D images
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from ...plots import generate_mask_colors, plot_contour, plot_image, save_image
from ...utils import (
    PathType,
    image_path_to_data_ax,
    mask_path_to_data_ax,
    path_in,
    save_path_file,
    significant_slice_idx_data,
)


def image_mask_annotated_path(
    image_path: PathType,
    mask_path: PathType,
    cmap="gray",
    save_path=None,
    limit: int = 10,
):
    image_path = path_in(image_path)
    mask_path = path_in(mask_path)

    image_data = image_path_to_data_ax(image_path)
    mask_data = mask_path_to_data_ax(mask_path)

    image_mask_annotated_array(
        image_data=image_data,
        mask_data=mask_data,
        cmap=cmap,
        save_path=save_path,
        limit=limit,
    )


def image_mask_annotated_array(
    image_data,
    mask_data,
    cmap="gray",
    save_path=None,
    limit: int = 10,
):
    print("Loading images...")

    most_value_nonzero_slices, num_nonzero_slices = significant_slice_idx_data(
        mask_data
    )
    num_masks = min(num_nonzero_slices, limit)

    rows = math.ceil(math.sqrt(num_masks))  # Number of rows in the grid
    columns = math.ceil(num_masks / rows)  # Number of columns in the grid

    mask_colors = generate_mask_colors(num_masks)

    _, axs = plt.subplots(rows, columns)

    if num_masks == 1:
        axs = np.array([axs])

    for i, ax in enumerate(axs.flat):
        if i < num_masks:
            # title = titles[i] if titles else f"Image {i}"
            plot_image(ax, image_data[:, :, most_value_nonzero_slices[i]], cmap=cmap)
            plot_contour(
                ax,
                mask_data[:, :, most_value_nonzero_slices[i]],
                color=mask_colors[i],
                levels=[0.5],
            )
            ax.set_title(f"Slice {most_value_nonzero_slices[i]}")
            # ax.axis("off")
        else:
            ax.axis("off")

    plt.tight_layout()

    if save_path:
        save_path = save_path_file(save_path, suffix=".png")
        save_image(plt, save_path)
    else:
        plt.show()

    plt.close()
