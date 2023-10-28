import medviz as viz

nii_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/1-1.nii"
niigz_path = (
    "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/cortical_bone.nii.gz"
)
mha_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/Rectal.mha"
dcm_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/rt.dcm"

images = viz.im2arr(nii_path, niigz_path, mha_path, dcm_path)

viz.profile(images)
