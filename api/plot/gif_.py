import medviz as viz

print(viz.__version__)
print(f"Make sure you have medviz version >= 1.1.4")

viz.gif(
    image="/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1.nii",
    masks=[
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1-label.nii",
        "/storage/sync/git/mohsen/medviz/test_local/dataset/plots/1-1-label.nii",
    ],
    start_slice=40,
    end_slice=50,
    # slices=[10, 40, 90, 100],
    save_path="her/1-1.gif",
    segments_title=["aaaaa", "saaa"],
)
