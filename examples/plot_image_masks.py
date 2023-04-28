"""

This script shows how to use the medviz module to visualize medical images and masks.
After installing medviz, this script can be run.

"""
import medviz


medviz.layered_plot(
    image_path="dataset/1-1.nii",
    mask_paths=["dataset/small_bowel.nii"],
    mask_colors=["red"],
    title="Layered Plot",
)

medviz.layered_plot(
    image_path="dataset/1-1.nii",
    mask_paths=["dataset/small_bowel.nii", "dataset/1-1-label.nii"],
    mask_colors=["red", "yellow"],
    title="Layered Plot",
)

medviz.layered_plot(
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
