### Support for metadata extraction from images
# .dcm, .nii, .nii.gz, .mha
import medviz as viz

image_nii = "/storage/sync/git/mohsen/medviz/test_local/dataset/images/1-1.nii"
image_dicom = "/storage/sync/git/mohsen/medviz/test_local/dataset/images/rt .dcm"
image_mha = "/storage/sync/git/mohsen/medviz/test_local/dataset/images/PROV_RectalCA_001_pre_ax_T2_raw.mha"


viz.metadata(image_nii)
viz.metadata(image_dicom)
viz.metadata(image_mha)
