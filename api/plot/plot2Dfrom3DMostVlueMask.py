from pathlib import Path

import medviz as viz

viz.plot2d_image_mask_annotated_path(
    image_path="dataset/1-1.nii", mask_path="dataset/1-1-label.nii", limit=20
)
