import matplotlib.pyplot as plt
import matplotlib.widgets as gui

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)

from pathlib import Path
import nibabel as nib


def type_checker(path):
    if not isinstance(path, Path):
        if isinstance(path, str):
            path = Path(path)
        else:
            raise Exception("Input must be a path.")

    data = nib.load(path).get_fdata()

    return data


def plot_image_mask(path_image, path_mask) -> str:
    image = type_checker(path_image)
    mask = type_checker(path_mask)
    print(image.shape)
    print(mask.shape)

    return image, mask


image, mask = plot_image_mask(
    path_image="/media/mohsen/My Passport/dataset/IBSI/ibsi_1_ct_radiomics_phantom/nifti/image/phantom.nii.gz",
    path_mask="/media/mohsen/My Passport/dataset/IBSI/ibsi_1_ct_radiomics_phantom/nifti/mask/mask.nii.gz",
)


m, n, d = image.shape


def sanity_check(image, mask):
    if image.shape != mask.shape:
        raise Exception("The shape of image and mask don't match.")


sanity_check(image, mask)


transparency_alpha = 0.2

init_slice_axial = 3
init_slice_coronal = 4
init_slice_sagittal = 5

plane = 0

im_init = image[init_slice_axial, :, :]
mask_init = mask[init_slice_axial, :, :]

ax.imshow(im_init, cmap="gray")
ax.imshow(mask_init, cmap="jet", alpha=transparency_alpha)


ax_slice = plt.axes([0.25, 0.2, 0.65, 0.03])
slider_slice = gui.Slider(
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
        ax.imshow(mask[slide, :, :], cmap="jet", alpha=transparency_alpha)

    elif plane == 1:
        ax.imshow(image[:, slide, :], cmap="gray")
        ax.imshow(mask[:, slide, :], cmap="jet", alpha=transparency_alpha)

    else:
        ax.imshow(image[:, :, slide], cmap="gray")
        ax.imshow(mask[:, :, slide], cmap="jet", alpha=transparency_alpha)


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
