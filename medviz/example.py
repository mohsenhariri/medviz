import medviz



# medviz.layered_plot("data/ct.nii.gz", ["data/lung_mask.nii.gz", "data/heart_mask.nii.gz"], ["red", "yellow"], "Layered Plot")

medviz.layered_plot(image_path="dataset/1-1.nii", mask_paths=["dataset/small_bowel.nii"], mask_colors=["red"], title="Layered Plot")

medviz.layered_plot(image_path="dataset/1-1.nii", mask_colors=["red", "yellow"], title="Layered Plot")


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


medviz.gif(
    image_path="dataset/1-1.nii",
    mask_paths=[
        "dataset/small_bowel.nii",
        "dataset/1-1-label.nii",
        "dataset/vertebrae_L3.nii.gz",
        "dataset/vertebrae_L4.nii.gz",
        "dataset/vertebrae_L5.nii.gz",
    ],
    mask_colors=["red", "yellow", "green", "blue", "purple"],
    title="Expert Annotations",
    interval=70,
    start_slice=30,
    end_slice=130,
    save_path="animation.gif",
)

