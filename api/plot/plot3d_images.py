import medviz as viz

viz.plot3d_images_path(
    paths=[
        "dataset/1-1.nii",
    ]
)
viz.plot3d_images_path(paths=["dataset/1-1.nii", "dataset/2-1.nii", "dataset/3-1.nii"])
viz.plot3d_images_path(paths=["dataset/1-1.nii", "dataset/1-1-label.nii"])


ct_data = viz.image_path_to_data_ax("dataset/1-1.nii")
viz.plot3d_images_array([ct_data, ct_data], titles=["Image", "Image"], cmap="gray")
