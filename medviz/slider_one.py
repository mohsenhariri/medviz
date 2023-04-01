import matplotlib.pyplot as plt
import matplotlib.widgets as gui

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)

from pathlib import Path

import nibabel as nib

def plot_nii(path):
    if not isinstance(path, Path):
        if isinstance(path, str):
            path = Path(path)
        else:
            raise Exception("Input must be a path.")

    image = nib.load(path)

    return image.get_fdata()

image = plot_nii(
    "/media/mohsen/My Passport/dataset/IBSI/ibsi_1_ct_radiomics_phantom/nifti/image/phantom.nii.gz"

)

image = plot_nii(
    "/media/mohsen/Mohsen2/share/Assets/Data/Florian_processed/labels_Res/349076_AX-HASTE-ng-lower-label_Res.nii"

)


print(image.shape)
m, n, d = image.shape

init_slice_axial = 3
init_slice_coronal = 4
init_slice_sagittal = 5

plane = 0

im_init = image[init_slice_axial, :, :]
ax.imshow(im_init, cmap="gray")

ax_slice = plt.axes([0.25, 0.2, 0.65, 0.03])
slider_slice =gui.Slider(
    ax=ax_slice,
    label="Slice",
    valmin=1,
    valmax=m - 2,
    valstep=2,
    valinit=init_slice_axial,
)


def update(e):
    slide = int(slider_slice.val)
    if plane == 0:
        ax.imshow(image[slide, :, :], cmap="gray")
    elif plane == 1:
        ax.imshow(image[:, slide, :], cmap="gray")
    else:
        ax.imshow(image[:, :, slide], cmap="gray")

slider_slice.on_changed(update)


ax_axial = plt.axes([0.1, 0.025, 0.1, 0.04])
ax_coronal = plt.axes([0.25, 0.025, 0.1, 0.04])
ax_sagittal = plt.axes([0.4, 0.025, 0.1, 0.04])
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])

btn_axial = gui.Button(ax_axial, "Axial", color="red", hovercolor="skyblue")
btn_coronal = gui.Button(ax_coronal, "Coronal", color="red", hovercolor="skyblue")
btn_sagittal = gui.Button(ax_sagittal, "Sagittal", color="red", hovercolor="skyblue")
btn_reset = gui.Button(ax_reset, "Reset", color="gold", hovercolor="skyblue")

def handle_axial(e):
    global plane
    plane = 0
    slider_slice.valmax = m - 2
    slider_slice.valinit = init_slice_axial
    slider_slice.reset()
    plt.suptitle("Axial")


def handle_coronal(e):
    global plane
    plane = 1
    slider_slice.valmax = n - 2
    slider_slice.valinit = init_slice_coronal
    slider_slice.reset()
    plt.suptitle("Coronal")


def handle_sagittal(e):
    global plane
    plane = 2
    slider_slice.valmax = d - 2
    slider_slice.valinit = init_slice_sagittal
    slider_slice.reset()
    plt.suptitle("Sagittal")

def handle_reset(e):
    slider_slice.reset()


btn_axial.on_clicked(handle_axial)
btn_coronal.on_clicked(handle_coronal)
btn_sagittal.on_clicked(handle_sagittal)

btn_reset.on_clicked(handle_reset)

plt.suptitle("Axial")

plt.show()
