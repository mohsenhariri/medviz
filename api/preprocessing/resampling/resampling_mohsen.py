import medviz as viz

im = "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/moshen/1-1.nii"
mask = (
    "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/moshen/1-1-label.nii"
)

viz.resample(im, method="trilinear", voxel_size=[1, 1, 1])
viz.resample(mask, method="nearest", voxel_size=[1, 1, 1])

im_resampled = "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/moshen/1-1_resampled_trilinear.nii"
mask_resampled = "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/moshen/1-1-label_resampled_nearest.nii"

print(f"Original image shape: {im.shape}")
print(f"Resampled image shape: {im_resampled.shape}")

print(f"Original mask shape: {mask.shape}")
print(f"Resampled mask shape: {mask_resampled.shape}")
