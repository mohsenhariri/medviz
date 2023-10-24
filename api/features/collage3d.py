from pathlib import Path

import medviz as viz

image_path = Path("dataset/crohn/fat/grp1/ct_resampled/32/32-1.nii")
mask_path = Path("dataset/crohn/fat/grp1/ti_resampled/32-1-label.nii")


image, mask = viz.read_image_mask(image=image_path, mask=mask_path)

viz.feats.collage3d(
    image,
    mask,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="/path/to/save",
    out_name="out_name",
)
