from pathlib import Path

import medviz as viz

image_path = Path(
    "/storage/sync/git/mohsen/medviz/test_local/dataset/pc/349090_CTE_AX_Res.nii"
)
mask_path = Path(
    "/storage/sync/git/mohsen/medviz/test_local/dataset/pc/349090_CTE_AX-ng-label_Res.nii"
)

# read image and mask without normalization
image, mask = viz.read_image_mask(image=image_path, mask=mask_path)

## read image and mask with normalization to [min, max] for the image
# image, mask = viz.read_image_mask(image=image_path, mask=mask_path, norm=True)

## read image and mask with normalization to [mean, std] for the image
# image, mask = viz.read_image_mask(image=image_path, mask=mask_path, norm=(0, 1))


## If mask is not a binary mask, you can use zero_out function to convert it to a binary mask.
# mask = viz.utils.zero_out(mask, 1) # zero out all values except 1
# mask = viz.utils.zero_out(mask, 2) # zero out all values except 2

viz.feats.collage3d(
    image, mask, window_sizes=[3, 5, 7, 9, 11], save_path="col3_cd", out_name="whole"
)

viz.feats.collage3d(
    image,
    mask,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="col3_cd",
    out_name="pad11",
    padding=True,
)


viz.feats.collage3d(
    image,
    mask,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="col3d_cd",
    out_name="pad20",
    padding=20,
)
