import medviz as viz

im_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/mike/PROV_COR_017_0000.mha"
mask_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/mike/PROV_COR_017.mha"

viz.resample(im_path, method="trilinear", voxel_size=[1, 1, 1])
viz.resample(mask_path, method="nearest", voxel_size=[1, 1, 1])

im_resampled_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/mike/PROV_COR_017_0000_resampled_trilinear.mha"
mask_resampled_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/resampling/mike/PROV_COR_017_resampled_nearest.mha"


im = viz.im2arr(im_path)
im_resampled = viz.im2arr(im_resampled_path)

mask = viz.im2arr(mask_path)
mask_resampled = viz.im2arr(mask_resampled_path)

print(f"Original image shape: {im.shape}")
print(f"Resampled image shape: {im_resampled.shape}")

print(f"Original mask shape: {mask.shape}")
print(f"Resampled mask shape: {mask_resampled.shape}")
