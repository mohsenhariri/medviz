import medviz as viz

viz.plot_image_path(
    image_path="dataset/1-1.nii",
    title="Plot",
)


import nibabel as nib
import numpy as np

image = nib.load("dataset/1-1.nii").get_fdata()
image = np.flip(np.rot90(image, k=1, axes=(0, 1)), axis=0)


viz.plot_image_data(image_data=image)
