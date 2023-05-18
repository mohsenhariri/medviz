from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import medviz as viz

image_path_to_data = viz.image_path_to_data
plot_image = viz.plot_image


def plot_image_path(image_path, title="Image", save_path=None):
    image_data = image_path_to_data(image_path)

    plot_image_data(
        image_data,
        title=title,
        save_path=save_path,
    )


def plot_image_data(image_data, title="Image", save_path=None):
    print("Loading images...")

    d = image_data.shape[2]
    init_slice, last_slice = d // 2, d - 1

    _, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    plot_image(ax, image_data[:, :, init_slice], cmap="gray")

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
