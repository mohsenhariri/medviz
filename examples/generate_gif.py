import medviz

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
    save_path=r"./output/animation.gif",
)
