import secrets
from pathlib import Path
from typing import Union

import numpy as np
import SimpleITK as sitk

from ..utils import path_in


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
            # image = path_in(image)
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
