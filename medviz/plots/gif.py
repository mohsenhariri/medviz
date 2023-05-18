# DocString: Create a gif from a 3D image and multiple 3D masks
"""
Create a gif from a 3D image and multiple 3D masks

Parameters
----------
image_path : str
    Path to the 3D image
mask_paths : list
    List of paths to the 3D masks
mask_colors : list  
    List of colors for each mask
interval : int, optional    
    Interval between frames in milliseconds (default is 100)
start_slice : int, optional
    Starting slice (default is 0)
end_slice : int, optional
    Ending slice (default is None)
title : str, optional
    Title of the gif (default is "Layered Plot")
save_path : str, optional
    Path to save the gif (default is "animation.gif")

Returns
-------
None

"""

from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import medviz as viz

assert_shape = viz.assert_shape

image_path_to_data = viz.image_path_to_data_ax
mask_path_to_data = viz.mask_path_to_data_ax

generate_mask_colors = viz.generate_mask_colors

mask_expand = viz.mask_expand

# def assert_shape(arr):
#     # image shape
#     n, m, d = arr[0].shape
#     try:
#         for np_array in arr:
#             assert np_array.shape == (m, n, d)
#     except AssertionError:
#         raise ValueError("All segments must have the same shape as the image")

#     return d // 2, d - 1


def gif(
    image_path,
    mask_paths,
    mask_colors=None,
    interval=100,
    start_slice=0,
    end_slice=None,
    title="",
    segments=None,
    save_path=None,
):
    ct_data = image_path_to_data(image_path)

    masks_data = []
    for mask_path in mask_paths:
        mask_data = mask_path_to_data(mask_path)
        masks_data.append(mask_data)

    num_masks = len(masks_data)

    if segments:
        try:
            assert len(segments) == num_masks
        except AssertionError:
            # raise ValueError("Number of segments must be equal to the number of masks")
            print(
                "Number of segments must be equal to the number of masks, segments will be ignored"
            )
            segments = None

    # _, last_slice = assert_shape(ct_data + masks_data)
    last_slice = ct_data.shape[-1] - 1

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    fig = plt.figure()

    end_slice = last_slice if end_slice is None else end_slice

    slice_range = range(start_slice, end_slice)

    def update_slice(frame):
        global current_slice

        current_slice = frame

        plt.clf()

        plt.imshow(ct_data[:, :, current_slice], cmap="gray")

        xbar_title = ""

        for i in range(len(masks_data)):
            if not np.all(masks_data[i][:, :, current_slice] == False):
                xbar_title_update = (
                    f"{segments[i]}: {mask_colors[i]}"
                    if segments
                    else f"Mask {i}: {mask_colors[i]}"
                )
                xbar_title = xbar_title + xbar_title_update

            plt.contour(
                masks_data[i][:, :, current_slice],
                colors=mask_colors[i],
                levels=[0.5],
            )

        plt.title(f"{title} Slice {current_slice} {xbar_title}")
        plt.axis("off")

    ani = animation.FuncAnimation(
        fig, update_slice, frames=slice_range, interval=interval
    )

    if save_path:
        if isinstance(save_path, str):
            save_path = Path(save_path)

        if save_path.suffix != ".png":
            save_path = save_path.with_suffix(".gif")

        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        ani.save(save_path, writer="pillow")

    plt.show()


def gif_slices(
    image_path,
    mask_paths,
    slices,
    mask_colors=None,
    interval=100,
    title="",
    segments=None,
    save_path=None,
):
    ct_data = image_path_to_data(image_path)

    masks_data = []
    for mask_path in mask_paths:
        mask_data = mask_path_to_data(mask_path)
        masks_data.append(mask_data)

    num_masks = len(masks_data)

    if segments:
        try:
            assert len(segments) == num_masks
        except AssertionError:
            # raise ValueError("Number of segments must be equal to the number of masks")
            print(
                "Number of segments must be equal to the number of masks, segments will be ignored"
            )
            segments = None

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    fig = plt.figure()

    def update_slice(frame):
        global current_slice

        current_slice = frame

        plt.clf()

        plt.imshow(ct_data[:, :, current_slice], cmap="gray")

        xbar_title = ""

        for i in range(len(masks_data)):
            if not np.all(masks_data[i][:, :, current_slice] == False):
                xbar_title_update = (
                    f"{segments[i]}: {mask_colors[i]}"
                    if segments
                    else f"Mask {i}: {mask_colors[i]}"
                )
                xbar_title = xbar_title + xbar_title_update

            plt.contour(
                masks_data[i][:, :, current_slice],
                colors=mask_colors[i],
                levels=[0.5],
            )

        plt.title(f"{title} Slice {current_slice} {xbar_title}")
        plt.axis("off")

    ani = animation.FuncAnimation(fig, update_slice, frames=slices, interval=interval)

    if save_path:
        if isinstance(save_path, str):
            save_path = Path(save_path)

        if save_path.suffix != ".png":
            save_path = save_path.with_suffix(".gif")

        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        ani.save(save_path, writer="pillow")

    plt.show()


def gif_non(
    image_path,
    mask_paths,
    mask_colors=None,
    interval=100,
    title="",
    segments=None,
    save_path=None,
):
    ct_data = image_path_to_data(image_path)

    masks_data = []
    slices = set()
    for mask_path in mask_paths:
        mask_data = mask_path_to_data(mask_path)
        most_value_nonzero_slices, _ = viz.significant_slice_idx_data(mask_data)
        slices.update(most_value_nonzero_slices)
        masks_data.append(mask_data)

    num_masks = len(masks_data)

    if segments:
        try:
            assert len(segments) == num_masks
        except AssertionError:
            # raise ValueError("Number of segments must be equal to the number of masks")
            print(
                "Number of segments must be equal to the number of masks, segments will be ignored"
            )
            segments = None

    # assert_shape(ct_data + masks_data)

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    fig = plt.figure()

    slice_range = slices

    def update_slice(frame):
        global current_slice

        current_slice = frame

        plt.clf()

        plt.imshow(ct_data[:, :, current_slice], cmap="gray")

        xbar_title = ""

        for i in range(len(masks_data)):
            if not np.all(masks_data[i][:, :, current_slice] == False):
                xbar_title_update = (
                    f"{segments[i]}: {mask_colors[i]}"
                    if segments
                    else f"Mask {i}: {mask_colors[i]}"
                )
                xbar_title = xbar_title + xbar_title_update

            plt.contour(
                masks_data[i][:, :, current_slice],
                colors=mask_colors[i],
                levels=[0.5],
            )

        plt.title(f"{title} Slice {current_slice} {xbar_title}")
        plt.axis("off")

    ani = animation.FuncAnimation(
        fig, update_slice, frames=slice_range, interval=interval
    )

    if save_path:
        if isinstance(save_path, str):
            save_path = Path(save_path)

        if save_path.suffix != ".png":
            save_path = save_path.with_suffix(".gif")

        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        ani.save(save_path, writer="pillow")

    plt.show()


def gif_reference(
    image_path,
    mask_reference_path,
    mask_paths,
    segments,
    mask_expert_cmap="jet",
    mask_colors=None,
    interval=100,
    title="Layered Plot",
    save_path="animation.gif",
):
    ct_data = image_path_to_data(image_path)

    mask_reference_data = mask_path_to_data(mask_reference_path)
    slices, _ = viz.significant_slice_idx_data(mask_reference_data)

    masks_data = []
    for mask_path in mask_paths:
        mask_data = mask_path_to_data(mask_path)
        masks_data.append(mask_data)

    num_masks = len(masks_data)

    if segments:
        try:
            assert len(segments) == num_masks
        except AssertionError:
            # raise ValueError("Number of segments must be equal to the number of masks")
            print(
                "Number of segments must be equal to the number of masks, segments will be ignored"
            )
            segments = None

    assert_shape(ct_data + mask_reference_data + masks_data)

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    fig = plt.figure()

    def update_slice(frame):
        global current_slice

        current_slice = frame

        plt.clf()

        plt.imshow(ct_data[:, :, current_slice], cmap="gray")

        plt.imshow(
            mask_reference_data[:, :, current_slice],
            cmap=mask_expert_cmap,
            alpha=0.3,
        )

        xbar_title = ""

        for i in range(len(masks_data)):
            if not np.all(masks_data[i][:, :, current_slice] == False):
                xbar_title_update = (
                    f"{segments[i]}: {mask_colors[i]}"
                    if segments
                    else f"Mask {i}: {mask_colors[i]}"
                )
                xbar_title = xbar_title + xbar_title_update

            plt.contour(
                masks_data[i][:, :, current_slice],
                colors=mask_colors[i],
                levels=[0.5],
            )

        plt.title(f"{title} Slice {current_slice} {xbar_title}")
        plt.axis("off")

    ani = animation.FuncAnimation(fig, update_slice, frames=slices, interval=interval)

    if save_path:
        if isinstance(save_path, str):
            save_path = Path(save_path)

        if save_path.suffix != ".png":
            save_path = save_path.with_suffix(".gif")

        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        ani.save(save_path, writer="pillow")

    plt.show()
