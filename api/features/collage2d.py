from pathlib import Path

import medviz as viz

image_path = Path("dataset/MPData/Axial_Image_NPY/Patient-002_ax_ls.npy")
mask_path = Path("dataset/MPData/Axial_Fat_NPY/Patient-002_ax_label_fat_ls.npy")


image, mask = viz.read_image_mask(image=image_path, mask=mask_path)

# viz.feats.collage2d(image, mask, window_sizes=[3, 5, 7, 9, 11], save_path="/path/to/save", out_name="out_name")

viz.feats.collage2d(
    image,
    mask,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="./save_collage",
    out_name="out_name",
)
