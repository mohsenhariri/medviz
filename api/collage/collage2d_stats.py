from pathlib import Path

import medviz as viz

image = Path(
    "/storage/sync/git/mohsen/medviz/test_local/dataset/gargi/MRE_005__BH_AX_Res_ISO_crp.nii"
)

mask = Path(
    "/storage/sync/git/mohsen/medviz/test_local/dataset/gargi/MRE_005_-H_AX__annotation_crp.nii"
)

image, mask = viz.read_image_mask(image=image, mask=mask)

stats = viz.utils.slice_stats(mask)

slice_min = stats["min"]
slice_max = stats["max"]
slice_median = stats["median"]

mask2d_min = mask[:, :, slice_min]
mask2d_max = mask[:, :, slice_max]
mask2d_median = mask[:, :, slice_median]

image2d_min = image[:, :, slice_min]
image2d_max = image[:, :, slice_max]
image2d_median = image[:, :, slice_median]


viz.feats.collage2d(
    image=image2d_min,
    mask=mask2d_min,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="./save_stack",
    out_name="min",
)

viz.feats.collage2d(
    image=image2d_max,
    mask=mask2d_max,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="./save_stack",
    out_name="max",
)

viz.feats.collage2d(
    image=image2d_median,
    mask=mask2d_median,
    window_sizes=[3, 5, 7, 9, 11],
    save_path="./save_stack",
    out_name="median",
)
