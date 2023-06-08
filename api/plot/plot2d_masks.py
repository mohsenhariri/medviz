from pathlib import Path
import medviz as viz
import nibabel as nib

ct_image = nib.load("dataset/1-1.nii")
ct_data = ct_image.get_fdata()

mask_path = Path("dataset/2d/masks/1-1-label_slice_1.nii.gz")
ct_mask = nib.load("dataset/1-1.nii")
mask_data = ct_mask.get_fdata()

# viz.plot2d_masks_path(paths=[mask_path])

viz.plot2d_masks_array(masks_data=[ct_data[:, :, 40] > 0.5, ct_data[:, :, 60] > 0.5, ct_data[:, :, 80] > 0.5])

viz.plot2d_masks_path(paths=["dataset/2d/masks/1-1-label_slice_1.nii.gz"])
viz.plot2d_masks_path(
    paths=[
        "dataset/2d/masks/1-1-label_slice_1.nii.gz",
        "dataset/2d/masks/1-1-label_slice_2.nii.gz",
        "dataset/2d/masks/1-1-label_slice_3.nii.gz",
    ],
    titles=["S_40", "S_60", "S_80"],
    mask_colors=["red", "green", "blue"],
)
