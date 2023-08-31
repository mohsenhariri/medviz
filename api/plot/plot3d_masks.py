import medviz as viz

viz.plot3d_masks_path(
    paths=[
        "dataset/1-1-label.nii",
    ]
)

viz.plot3d_masks_path(paths=["dataset/1-1-label.nii", "dataset/small_bowel.nii.gz"])


mask1_data = viz.mask_path_to_data_ax("dataset/small_bowel.nii.gz")
mask2_data = viz.mask_path_to_data_ax("dataset/1-1-label.nii")

viz.plot3d_masks_array(
    masks_data=[mask1_data, mask2_data],
    titles=["Small Bowel", "TI"],
    mask_colors=["red", "blue"],
)
