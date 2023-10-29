from io import BytesIO
from pathlib import Path
from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from ..utils import path_in, save_path_file
from .plot_helpers import _generate_mask_colors, _read_images, _read_masks


def gif(
    image: Union[str, Path, np.ndarray],
    masks: Optional[
        Union[str, Path, np.ndarray, List[Union[str, Path, np.ndarray]]]
    ] = None,
    mask_colors: Optional[List[str]] = None,
    segments_title: Optional[List[str]] = None,
    start_slice: Optional[int] = 0,
    end_slice: Optional[int] = None,
    slices: Optional[List[int]] = None,
    cmap: str = "gray",
    plane: str = "axial",
    save_path: Union[str, Path] = "output.gif",
    duration: int = 100,  # Duration for each frame in the GIF (in milliseconds)
) -> None:
    
    """
    Creates a GIF animation from slices of a 3D image, with optional mask overlays.

    Parameters:
    - image: Path or ndarray of the 3D image.
    - masks: List of paths or ndarrays of 3D masks to overlay on the image.
    - mask_colors: Colors for each mask. Default generates random colors.
    - start_slice: Starting slice index.
    - end_slice: Ending slice index.
    - slices: Specific slice indices to use. Overrides start_slice and end_slice.
    - cmap: Colormap for displaying the image. Default is 'gray'.
    - plane: Plane of the image ('axial', 'sagittal', or 'coronal').
    - save_path: Path to save the resulting GIF.
    - duration: Duration for each frame in the GIF (in milliseconds).
    - segments_title: Titles for each mask segment.

    Returns:
    - None: The function saves the resulting GIF to save_path.
    """
    
    image_data = _read_images(image, plane=plane)
    if masks:
        masks_data = _read_masks(masks, plane=plane)
        mask_colors = _generate_mask_colors(len(masks_data), mask_colors)
    else:
        masks_data = [None] * len(image_data)
        mask_colors = [None] * len(image_data)

    if segments_title:
        if len(segments_title) != len(masks_data):
            print(
                "Number of segments must be equal to the number of masks, segments will be ignored"
            )
            segments_title = None

    # Validate slice indices and set defaults if not provided

    # if end_slice is None:
    #     end_slice = image_data[0].shape[0] - 1
    # end_slice = image_data[0].shape[0] - 1 if end_slice is None else end_slice

    if slices:
        slice_range = slices
    else:
        end_slice = image_data[0].shape[0] - 1 if end_slice is None else end_slice
        slice_range = range(start_slice, end_slice + 1)

    # List to store individual frames for the GIF
    frames = []

    # For each slice of the 3D image between start_slice and end_slice
    for slice_idx in slice_range:
        fig, ax = plt.subplots()

        # Display the image slice
        ax.imshow(image_data[0][slice_idx], cmap=cmap)
        title_str = ""

        # Overlay each mask on the image
        for i, mask in enumerate(masks_data):
            if mask is not None:
                ax.contour(mask[slice_idx], colors=mask_colors[i], levels=[0.5])
                if segments_title:
                    title_str += f"{segments_title[i]}: {mask_colors[i]}  "

        if segments_title:
            ax.set_title(title_str)
        ax.axis("off")

        # Convert the Matplotlib figure to a PIL Image without saving it to a file
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
        buf.seek(0)
        frame = Image.open(buf)
        frames.append(frame)

        # Close the figure to free up memory
        plt.close(fig)

    # Save frames as a GIF
    gif_path = save_path_file(save_path, "gif")
    frames[0].save(
        gif_path, save_all=True, append_images=frames[1:], duration=duration, loop=0
    )
