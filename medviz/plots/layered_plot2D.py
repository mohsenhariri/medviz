from pathlib import Path

import matplotlib.pyplot as plt

import medviz as viz

assert_shape = viz.assert_shape
mask_path_to_data = viz.mask_path_to_data_ax
image_path_to_data = viz.image_path_to_data_ax
generate_mask_colors = viz.generate_mask_colors
plot_image = viz.plot_image
plot_contour = viz.plot_contour

significant_slice_idx_data = viz.significant_slice_idx_data


def layered_plot_path2D(
    image_path,
    mask_paths,
    slice,
    mask_colors=None,
    title="Layered Plot",
    save_path=None,
):
    image_data = image_path_to_data(image_path)

    masks_data = []
    for mask_path in mask_paths:
        mask_data = mask_path_to_data(mask_path)
        masks_data.append(mask_data)

    layered_plot_data2D(
        image_data,
        masks_data,
        mask_colors=mask_colors,
        slice=slice,
        title=title,
        save_path=save_path,
    )


def layered_plot_data2D(
    image_data,
    masks_data,
    slice,
    mask_colors=None,
    title="Layered Plot",
    save_path=None,
):
    print("Loading images...")

    num_masks = len(masks_data)

    assert_shape(image_data + masks_data)

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    _, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    plot_image(ax, image_data[:, :, slice], cmap="gray")

    for i in range(num_masks):
        plot_contour(ax, masks_data[i][:, :, slice], color=mask_colors[i], levels=[0.5])

    ax.set_xlabel(f"Slice Number: {slice}")
    ax.set_title(title)

    plt.show()

    if save_path:
        if isinstance(save_path, str):
            save_path = Path(save_path)

        if save_path.suffix != ".png":
            save_path = save_path.with_suffix(".png")

        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        plt.savefig(save_path)


import matplotlib.pyplot as plt
import numpy as np


def layered_plot_all2D(
    id, image_data, mask_data, save_path, mask_color="red", title=""
):
    image_data_rot = np.flip(np.rot90(image_data, axes=(1, 0)), axis=1)
    mask_data_rot = np.flip(np.rot90(mask_data, axes=(1, 0)), axis=1)

    most_value_nonzero_slices, num_nonzero_slices = significant_slice_idx_data(
        mask_data_rot
    )
    print(most_value_nonzero_slices, num_nonzero_slices)
    for i in range(num_nonzero_slices):
        slice = most_value_nonzero_slices[i]
        _, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        plot_image(ax, image_data_rot[:, :, slice], cmap="gray")
        plot_contour(ax, mask_data_rot[:, :, slice], color=mask_color, levels=[0.5])
        ax.set_xlabel(f"ID:{id} Slice Number: {slice}")
        ax.set_title(title)
        plt.tight_layout()

        plt.savefig(f"./crohns_plots/{id}_Slice_{slice}.png")
        plt.close()
    pass


import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("./crohn/image_mask.csv")
    for index, row in df.iterrows():
        id = row["ID"]
        print(id)
        print(type(id))

        if id != 51:
            image_path = row["Image"].replace("['", "").replace("']", "")
            mask_path = row["Mask"].replace("['", "").replace("']", "")
            print(image_path)
            print(mask_path)

            image_data = np.load(image_path)
            mask_data = np.load(mask_path)
            layered_plot_all2D(id, image_data, mask_data, save_path="layered_plot.png")

            pass
    # image_path = Path("data/image.nii.gz")
    # mask_paths = [Path("data/mask1.nii.gz"), Path("data/mask2.nii.gz")]

    # layered_plot_all2D(image_path, mask_paths,  save_path="layered_plot.png")
    # layered_plot_all2D(image_path, mask_paths,  save_path="crohns_plots")
