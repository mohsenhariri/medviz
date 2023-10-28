import medviz as viz

nii_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/1-1.nii"
niigz_path = (
    "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/cortical_bone.nii.gz"
)
mha_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/Rectal.mha"
dcm_path = "/storage/sync/git/mohsen/medviz/test_local/dataset/reader/rt.dcm"


nii = viz.im2arr(nii_path)
niigz = viz.im2arr(niigz_path)
mha = viz.im2arr(mha_path)
dcm = viz.im2arr(dcm_path)

print(f"Sahpe of nii: {nii.shape}")
print(f"Sahpe of niigz: {niigz.shape}")
print(f"Sahpe of mha: {mha.shape}")
print(f"Sahpe of dcm: {dcm.shape}")

print(f"Type of nii: {type(nii)}")
print(f"Type of niigz: {type(niigz)}")
print(f"Type of mha: {type(mha)}")
print(f"Type of dcm: {type(dcm)}")


# Read multiple images

nii, niigz, mha, dcm = viz.im2arr(nii_path, niigz_path, mha_path, dcm_path)

images = viz.im2arr(nii_path, niigz_path, mha_path, dcm_path)
for image in images:
    print(f"Shape: {image.shape}")
    print(f"Type: {type(image)}")

viz.profile(images)
