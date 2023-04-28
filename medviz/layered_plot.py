## Docstring: Layered plot of CT image and mask
"""

    Args:
        image_path (str): Path to CT image
        mask_paths (list): List of paths to masks
        mask_colors (list): List of colors for masks
        title (str): Title of plot

    Returns:
        None

    Examples:
        >>> import medviz
        >>> medviz.layered_plot("data/ct.nii.gz", ["data/lung_mask.nii.gz", "data/heart_mask.nii.gz"], ["red", "yellow"], "Layered Plot")

"""
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def layered_plot(image_path, mask_paths, mask_colors, title="Layered Plot"):
    print("Loading images...")

    ct_img = nib.load(image_path)
    ct_data = ct_img.get_fdata()
    ct_data = np.flip(np.rot90(ct_data, axes=(1, 0)), axis=1)

    mask_datas = []
    for mask_path in mask_paths:
        mask_data = nib.load(mask_path)
        mask_data = np.flip(np.rot90(mask_data.get_fdata(), axes=(1, 0)), axis=1)
        mask_datas.append(mask_data)

    _, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    ax.imshow(ct_data[:, :, ct_data.shape[2] // 2], cmap="gray")

    for i in range(len(mask_datas)):
        ax.contour(
            mask_datas[i][:, :, mask_datas[i].shape[2] // 2],
            colors=mask_colors[i],
            levels=[0.5],
        )

    ax.set_xlabel("Slice Number")
    ax.set_title(title)

    slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])

    slider = Slider(
        slider_ax,
        "Slice",
        0,
        ct_data.shape[2] - 1,
        valinit=ct_data.shape[2] // 2,
        valstep=1,
    )

    def update(val):
        slice_num = int(slider.val)
        ax.clear()
        ax.imshow(ct_data[:, :, slice_num], cmap="gray")
        for i in range(len(mask_datas)):
            ax.contour(
                mask_datas[i][:, :, slice_num], colors=mask_colors[i], levels=[0.5]
            )

        ax.set_xlabel("Slice Number")
        ax.set_title(title)

    slider.on_changed(update)

    plt.show()
