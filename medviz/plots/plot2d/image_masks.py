from filecmp import cmp

import matplotlib.pyplot as plt

from ...plots import (
    assert_shape,
    generate_mask_colors,
    plot_contour,
    plot_image,
    save_image,
)
from ...utils import (
    image_path_to_data_ax,
    mask_path_to_data_ax,
    path_in,
    save_path_file,
)


def image_masks_path(
    image_path,
    masks_path,
    mask_colors=None,
    titles=[],
    title_image="Image",
    cmap="gray",
    origin="upper",
    save_path=None,
):
    if len(masks_path) == 0:
        raise ValueError("masks_path must be a list of paths")

    image_path = path_in(image_path)
    image_data = image_path_to_data_ax(image_path)

    masks_path = [path_in(path) for path in masks_path]
    masks_data = [mask_path_to_data_ax(path) for path in masks_path]

    image_masks_array(
        image_data=image_data,
        masks_data=masks_data,
        mask_colors=mask_colors,
        titles=titles,
        title_image=title_image,
        cmap=cmap,
        origin=origin,
        save_path=save_path,
    )


def image_masks_array(
    image_data,
    masks_data,
    mask_colors=None,
    titles=[],
    title_image="Image",
    cmap="gray",
    origin="upper",
    save_path=None,
):
    if len(masks_data) == 0:
        raise ValueError("masks_data must be a list of arrays")

    print("Loading images...")

    if image_data.ndim != 2:
        raise ValueError("Image must be 2D")

    for mask_data in masks_data:
        if mask_data.ndim != 2:
            raise ValueError("Masks must be 2D")

    num_masks = len(masks_data)

    # assert_shape(image_data + masks_data)

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    _, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    plot_image(ax, image_data, cmap=cmap, origin=origin, title=title_image)

    for i in range(num_masks):
        title = titles[i] if titles else f"Mask {i}"
        plot_contour(
            ax,
            masks_data[i],
            color=mask_colors[i],
            title=title,
            origin=origin,
            levels=[0.5],
        )

    # ax.set_xlabel(f"Slice Number: {slice}")
    # ax.set_title(title)
    plt.tight_layout()

    if save_path:
        save_path = save_path_file(save_path, suffix=".png")
        save_image(plt, save_path)
    else:
        plt.show()

    plt.close()
