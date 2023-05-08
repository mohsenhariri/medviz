from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import medviz as viz

assert_shape = viz.assert_shape
mask_path_to_data = viz.mask_path_to_data
image_path_to_data = viz.image_path_to_data
generate_mask_colors = viz.generate_mask_colors
plot_image = viz.plot_image
plot_contour = viz.plot_contour


def layered_plot_path3D(
    image_path, mask_paths, mask_colors=None, title="Layered Plot", save_path=None
):
    image_data = image_path_to_data(image_path)

    masks_data = []
    for mask_path in mask_paths:
        mask_data = mask_path_to_data(mask_path)
        masks_data.append(mask_data)

    layered_plot_data3D(
        image_data,
        masks_data,
        mask_colors=mask_colors,
        title=title,
        save_path=save_path,
    )


def layered_plot_data3D(
    image_data, masks_data, mask_colors=None, title="Layered Plot", save_path=None
):
    print("Loading images...")

    init_slice, last_slice = assert_shape(image_data + masks_data)

    num_masks = len(masks_data)

    init_slice, last_slice = assert_shape(image_data + masks_data)

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    _, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    plot_image(ax, image_data[:, :, init_slice], cmap="gray")

    for i in range(num_masks):
        plot_contour(
            ax, masks_data[i][:, :, init_slice], color=mask_colors[i], levels=[0.5]
        )

    ax.set_xlabel(f"Slice Number: {init_slice}")
    ax.set_title(title)

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
        ax.clear()

        plot_image(ax, image_data[:, :, slice_num], cmap="gray")
        for i in range(num_masks):
            plot_contour(ax, masks_data[i][:, :, slice_num], color=mask_colors[i])

        ax.set_xlabel(f"Slice Number: {slice_num}")
        ax.set_title(title)

    slider.on_changed(update)

    plt.show()

    if save_path:
        if isinstance(save_path, str):
            save_path = Path(save_path)

        if save_path.suffix != ".png":
            save_path = save_path.with_suffix(".png")

        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        plt.savefig(save_path)
