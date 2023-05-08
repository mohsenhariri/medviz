import medviz as viz

viz.layered_plot_path3D(
    image_path="dataset/1-1.nii",
    mask_paths=["dataset/small_bowel.nii"],
    mask_colors=["red"],
    title="Layered Plot",
)

viz.layered_plot_path3D(
    image_path="dataset/1-1.nii",
    mask_paths=["dataset/small_bowel.nii", "dataset/1-1-label.nii"],
    mask_colors=["red", "yellow"],
    title="Layered Plot",
)

viz.layered_plot_path3D(
    image_path="dataset/1-1.nii",
    mask_paths=[
        "dataset/small_bowel.nii",
        "dataset/1-1-label.nii",
        "dataset/vertebrae_L3.nii.gz",
        "dataset/vertebrae_L4.nii.gz",
        "dataset/vertebrae_L5.nii.gz",
    ],
    mask_colors=["red", "yellow", "green", "blue", "purple"],
    title="Layered Plot",
)

# without mask colors
viz.layered_plot_path3D(
    image_path="dataset/1-1.nii",
    mask_paths=["dataset/small_bowel.nii"],
)

viz.layered_plot_path3D(
    image_path="dataset/1-1.nii",
    mask_paths=[
        "dataset/small_bowel.nii",
        "dataset/1-1-label.nii",
        "dataset/vertebrae_L3.nii.gz",
        "dataset/vertebrae_L4.nii.gz",
        "dataset/vertebrae_L5.nii.gz",
    ],
)

# layered_plot_data3D

import nibabel as nib
import numpy as np

image = nib.load("dataset/1-1.nii").get_fdata()
image = np.flip(np.rot90(image, k=1, axes=(0, 1)), axis=0)

mask_bowel = nib.load("dataset/small_bowel.nii").get_fdata()
mask_bowel = np.flip(np.rot90(mask_bowel, k=1, axes=(0, 1)), axis=0)

viz.layered_plot_data3D(image_data=image, masks_data=[mask_bowel])
