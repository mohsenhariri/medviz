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

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import nibabel as nib


def gif(
    image_path,
    mask_paths,
    mask_colors,
    interval=100,
    start_slice=0,
    end_slice=None,
    title="Layered Plot",
    save_path="animation.gif",
):
    img = nib.load(image_path)
    data = img.get_fdata()

    mask_imgs = []
    for mask_path in mask_paths:
        mask_imgs.append(nib.load(mask_path))

    masks_data = []
    for mask_img in mask_imgs:
        masks_data.append(mask_img.get_fdata())

    fig = plt.figure()

    end_slice = data.shape[2] if end_slice is None else end_slice

    slice_range = range(start_slice, data.shape[2])

    # Define the update function for the animation

    def update_slice(frame):
        global current_slice

        current_slice = frame

        plt.clf()

        plt.imshow(data[:, :, current_slice].T, cmap="gray")

        for i in range(len(masks_data)):
            plt.contour(
                masks_data[i][:, :, current_slice].T,
                colors=mask_colors[i],
                levels=[0.5],
            )

        plt.title(f"{title} Slice {current_slice}")
        plt.xlabel("X")

        plt.axis("off")

    ani = animation.FuncAnimation(
        fig, update_slice, frames=slice_range, interval=interval
    )

    ani.save(save_path, writer="pillow")

    plt.show()
