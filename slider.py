import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
r = 0.6

im = np.load("./355644.npy")

init_slice = 50
im_array = im[:, :, init_slice]
m, n, d = im.shape

ax.imshow(im_array, cmap="gray")

ax_slice = plt.axes([0.25, 0.2, 0.65, 0.03])

slider_slice = Slider(
    ax=ax_slice,
    label="Slice",
    valmin=1,
    valmax=d - 2,
    valstep=2,
    valinit=init_slice,
)


def update(val):
    slide = int(slider_slice.val)
    ax.imshow(im[:, :, slide], cmap="gray")


slider_slice.on_changed(update)


ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])


button = Button(ax_reset, "Reset", color="gold", hovercolor="skyblue")


def handle_reset(e):
    slider_slice.reset()


button.on_clicked(handle_reset)


plt.show()
