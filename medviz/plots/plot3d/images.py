import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

from ...utils import image_path_to_data_ax
from .. import plot_image_imshow


def images_path(paths, rows=None, columns=None, titles=[], cmap="gray"):
    images_data = [image_path_to_data_ax(path) for path in paths]

    images_array(
        images_data=images_data,
        rows=rows,
        columns=columns,
        titles=titles,
        cmap=cmap,
    )


def images_array(images_data, rows=None, columns=None, titles=[], cmap="gray"):
    print("Loading images...")

    d = images_data[0].shape[2]
    init_slice, last_slice = d // 2, d - 1

    num_images = len(images_data)  # Number of images
    rows = math.ceil(math.sqrt(num_images))  # Number of rows in the grid
    columns = math.ceil(num_images / rows)  # Number of columns in the grid

    _, axs = plt.subplots(rows, columns)
    if num_images == 1:
        axs = np.array([axs])

    plt.subplots_adjust(bottom=0.25)

    for i, ax in enumerate(axs.flat):
        if i < num_images:
            title = titles[i] if titles else f"Image {i}"
            plot_image_imshow(
                ax, images_data[i][:, :, init_slice], cmap=cmap, title=title
            )
            ax.axis("off")
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

                plot_image_imshow(
                    ax, images_data[i][:, :, slice_num], cmap=cmap, title=title
                )
                ax.set_xlabel(f"Slice Number: {slice_num}")
                ax.axis("off")
            else:
                ax.axis("off")

        # ax.set_title(title)

    slider.on_changed(update)

    plt.tight_layout()
    plt.show()


# import nibabel as nib

# if __name__ == "__main__":
#     ct_image = nib.load("dataset/1-1.nii")
#     ct_data = ct_image.get_fdata()
#     print(ct_data.shape)
#     ct_data = image_path_to_data("dataset/1-1.nii")
#     # ct_data = ct_data[:, :, 100]
#     plot_multi_data([ct_data, ct_data], title="Image")
