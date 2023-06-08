from pathlib import Path
import medviz as viz
import nibabel as nib


ct_image = nib.load("dataset/1-1.nii")
ct_data = ct_image.get_fdata()

viz.plot2d_images_array(images_data=[ct_data[:, :, 40]])
viz.plot2d_images_array(images_data=[ct_data[:, :, 40], ct_data[:, :, 60], ct_data[:, :, 80]])
viz.plot2d_images_array(
    images_data=[ct_data[:, :, 40], ct_data[:, :, 60], ct_data[:, :, 80]], titles=["T_40", "T_60", "T_80"]
)
viz.plot2d_images_array(
    images_data=[ct_data[:, :, 40], ct_data[:, :, 60], ct_data[:, :, 80]],
    titles=["T_40", "T_60", "T_80"],
    save_path="./savefigures/1.png",
)
viz.plot2d_images_array(
    images_data=[ct_data[:, :, 40], ct_data[:, :, 60], ct_data[:, :, 80]],
    titles=["L_40", "L_60", "L_80"],
    cmap="jet",
    origin="lower",
)


viz.plot2d_images_path(paths=["dataset/1-1-100-2D.nii"])
viz.plot2d_images_path(paths=["dataset/1-1-100-2D.nii", "dataset/1-1-100-2D.nii"], titles=["T_40", "T_60"])
viz.plot2d_images_path(
    paths=["dataset/1-1-100-2D.nii", "dataset/1-1-100-2D.nii"],
    titles=["T_40", "T_60"],
    save_path="./savefigures/2.png",
)
