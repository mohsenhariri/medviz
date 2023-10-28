import math
import secrets
from pathlib import Path
from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
from matplotlib.widgets import Slider

from ..utils import path_in, save_path_file

# mask_characteristics = mask_characteristics(mask_path)


def _generate_mask_colors(num_masks, mask_colors=None):
    if mask_colors is None:
        mask_colors = ["#" + secrets.token_hex(3) for _ in range(num_masks)]

        return mask_colors
    else:
        try:
            assert num_masks == len(mask_colors)
            return mask_colors
        except AssertionError:
            raise ValueError(
                f"Number of masks ({num_masks}) does not match number of colors ({len(mask_colors)})"
            )


def _read_images(images, plane="axial"):
    images_data = []
    if not isinstance(images, (list, tuple)):
        images = [images]
    for image in images:
        if isinstance(image, Union[str, Path]):
            image = path_in(image)
            image = sitk.ReadImage(str(image))
            image = sitk.GetArrayFromImage(image)

            if plane == "sagittal":
                image = image.transpose(1, 2, 0)
            elif plane == "coronal":
                image = image.transpose(2, 1, 0)

            images_data.append(image)
        elif isinstance(image, np.ndarray):
            images_data.append(image)
        else:
            raise ValueError("images must be a list of strings or numpy arrays")
    return images_data


def _read_masks(masks, plane="axial"):
    masks_data = []
    if masks is not None and not isinstance(masks, (list, tuple)):
        masks = [masks]

    for mask in masks:
        # if mask is not None and mask_characteristics(mask)["mask_type"] != "Binary":
        #     print(f"Mask {mask} is not binary.")

        if isinstance(mask, Union[str, Path]):
            mask = path_in(mask)
            mask = sitk.ReadImage(str(mask))
            mask = sitk.GetArrayFromImage(mask)
            if plane == "sagittal":
                mask = mask.transpose(1, 2, 0)
            elif plane == "coronal":
                mask = mask.transpose(2, 1, 0)

            masks_data.append(mask)
        elif isinstance(mask, np.ndarray):
            masks_data.append(mask)
        elif not mask:
            masks_data.append(mask)
        else:
            raise ValueError("masks must be a list of strings or numpy arrays")
    return masks_data


def plot3d(
    images: Union[str, Path, np.ndarray, List[Union[str, Path, np.ndarray]]],
    masks: Optional[
        Union[
            str,
            Path,
            np.ndarray,
            List[Union[str, Path, np.ndarray]],
        ]
    ] = None,
    rows: Optional[int] = None,
    columns: Optional[int] = None,
    mask_colors: Optional[List[str]] = None,
    cmap: str = "gray",
    titles: Optional[Union[str, List[str]]] = None,
    plane: str = "axial",
    save_path: Optional[Union[str, Path]] = None,
) -> None:
    images = _read_images(images, plane=plane)
    num_images = len(images)
    assert num_images > 0, "images cannot be empty"

    if masks:
        masks = _read_masks(masks, plane=plane)

        assert num_images == len(masks), "Number of images and masks must be equal"

        mask_colors = _generate_mask_colors(num_images, mask_colors)
    else:
        masks = [None] * num_images
        mask_colors = [None] * num_images

    if titles:
        assert num_images == len(titles), "Number of images and titles must be equal"
    else:
        titles = [f"Image {i}" for i in range(num_images)]

    if rows is None and columns is None:
        rows = math.ceil(math.sqrt(num_images))  # Number of rows in the grid
        columns = math.ceil(num_images / rows)  # Number of columns in the grid
    elif rows is None:
        rows = math.ceil(num_images / columns)
    elif columns is None:
        columns = math.ceil(num_images / rows)

    if num_images > rows * columns:
        raise ValueError("rows * columns must be greater than or equal to num_images")

    _, axs = plt.subplots(rows, columns)

    if num_images == 1:
        axs = np.array([axs])

    plt.subplots_adjust(bottom=0.25)

    sliders = []
    for i, ax in enumerate(axs.flat):
        if i < num_images:
            middle_slice = images[i].shape[0] // 2
            depth = images[i].shape[0]
            ax.imshow(images[i][middle_slice], cmap=cmap)
            if masks and masks[i] is not None:
                ax.contour(masks[i][middle_slice], colors=mask_colors[i], levels=[0.5])

            # title = titles[i] if titles else f"Image {i}"
            ax.set_title(titles[i])
            ax.set_xlabel(f"Slice Number: {middle_slice}")

            # slider_ax = plt.axes([0.1, 0.05 * (i + 1), 0.8, 0.03])
            # slider_position = ax.get_position()
            # slider_ax = plt.axes([slider_position.x0, slider_position.y0-0.1, slider_position.width, 0.03])

            slider_position = ax.get_position()
            slider_ax = plt.axes(
                [
                    slider_position.x0,
                    slider_position.y0 - 0.15,
                    slider_position.width,
                    0.03,
                ]
            )

            slider = Slider(
                slider_ax,
                f"Slice {i+1}",
                0,
                depth - 1,
                valinit=middle_slice,
                valstep=1,
            )
            sliders.append(slider)

            # print(slider_ax)

            def update(
                val,
                ax=ax,
                img=images[i],
                mask=masks[i],
                title=titles[i],
                # mask = None,
                slider=slider,
                color=mask_colors[i],
                # color = None,
            ):
                # if masks is not None:
                #     mask = masks[i]
                #     color = mask_colors[i]

                slice_num = int(slider.val)
                ax.clear()
                ax.imshow(img[slice_num], cmap=cmap)
                if mask is not None:
                    ax.contour(mask[slice_num], colors=color, levels=[0.5])

                ax.set_title(title)
                ax.set_xlabel(f"Slice Number: {slice_num}")

            slider.on_changed(update)
        else:
            ax.axis("off")

    plt.tight_layout()
    plt.show()

    if save_path:
        save_path = save_path_file(save_path, suffix=".png")
        plt.savefig(save_path)
    else:
        plt.show()

    plt.close()
