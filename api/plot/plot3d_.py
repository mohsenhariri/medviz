import medviz as viz

viz.plot3d("/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1.nii")

viz.plot3d(
    images=[
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1.nii",
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/rt.dcm",
    ],
    masks=[
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1-label.nii",
        None,
    ],
    rows=1,
    columns=2,
)

viz.plot3d(
    images=[
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1.nii",
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/rt.dcm",
    ],
    titles=["First ", "Second"],
    rows=1,
    columns=2,
)

viz.plot3d(
    images=[
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/349090_CTE_AX_Res.nii",
    ]
)

viz.plot3d(
    images="/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1.nii",
    masks="/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1-label.nii",
    plane="coronal",
)

viz.plot3d(
    images=[
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1.nii",
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/rt.dcm",
    ],
    masks=[
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1-label.nii",
        None,
    ],
    titles=["Image 1", "Image 2"],
    rows=1,
    columns=2,
)
