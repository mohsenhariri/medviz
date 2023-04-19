import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider





def layered_plot(image_path, mask_paths, mask_colors=["red", "yellow"], title="Layered Plot"):
    print("Loading images...")
# Load the CT scan and mask imagesfsdf
    ct_img = nib.load(image_path)
    mask_img1 = nib.load(mask_paths[0])
    mask_img2 = nib.load(mask_paths[1])

    # Get the image data and mask data
    ct_data = ct_img.get_fdata()
    mask_data1 = mask_img1.get_fdata()
    mask_data2 = mask_img2.get_fdata()

    # Rotate the images 90 degrees clockwise
    ct_data = np.rot90(ct_data, axes=(1, 0))
    mask_data1 = np.rot90(mask_data1, axes=(1, 0))
    mask_data2 = np.rot90(mask_data2, axes=(1, 0))

    # Create a figure with a slider
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    ax.imshow(ct_data[:, :, ct_data.shape[2]//2], cmap='gray')
    ax.contour(mask_data1[:, :, mask_data1.shape[2]//2], colors='r', levels=[0.5])
    ax.contour(mask_data2[:, :, mask_data2.shape[2]//2], colors='b', levels=[0.5])
    ax.set_xlabel('Slice Number')
    slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
    slider = Slider(slider_ax, 'Slice', 0, ct_data.shape[2]-1, valinit=ct_data.shape[2]//2, valstep=1)

    # Update the plot when the slider value changes
    def update(val):
        slice_num = int(slider.val)
        ax.clear()
        ax.imshow(ct_data[:, :, slice_num], cmap='gray')
        ax.contour(mask_data1[:, :, slice_num], colors='r', levels=[0.5])
        ax.contour(mask_data2[:, :, slice_num], colors='y', levels=[0.5])
        ax.set_xlabel('Slice Number')

    slider.on_changed(update)
    plt.show()
