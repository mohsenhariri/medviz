import medviz as viz
from pathlib import Path
import numpy as np

# image, mask = viz.read_image_mask(image=cor_image_path, mask=cor_mask_path)

print("Version:", viz.__version__)
print("Please make sure the version is 1.2.0 or higher.")

image_path = Path(
    "/storage/sync/git/mohsen/medviz/test_local/dataset/leo_MPData/Axial_Image_NPY/Patient-001_ax_ls.npy"
)
mask_path = Path(
    "/storage/sync/git/mohsen/medviz/test_local/dataset/leo_MPData/Axial_Fat_NPY/Patient-001_ax_label_fat_ls.npy"
)

image = np.load(image_path).astype(np.float64)
mask = np.load(mask_path).astype(np.float64)


viz.feats.collage2d(
    image,
    mask,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="./export_feats",
    out_name="id",
    feature_maps=True,  # Optional, default is False, if True it will save the feature maps in png format
    save_raw=False,  # Optional, default is False, if True it will save the raw features
)
