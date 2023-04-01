from time import strftime

import matplotlib.pyplot as plt


def now():
    return strftime("%m-%d-%Y_%H-%M-%S")


def plot(ax, img, title=None, cmap="gray", RGB=False):
    if RGB:
        cmap = None
        ax.axis("off")
    ax.imshow(img, cmap=cmap)
    ax.set_title(title)


def showRGB2(im1, im2, t1=None, t2=None, title=None, save_path=False):
    fig, axs = plt.subplots(1, 2)

    plot(axs[0], im1, title=t1, RGB=True)
    plot(axs[1], im2, title=t2, RGB=True)

    fig.suptitle(title, fontsize=16)
    plt.show()
    if save_path:
        current_time = now()
        plt.savefig(rf"{save_path}/fig-{current_time}")


def showRGB4(
    im1, im2, im3, im4, t1=None, t2=None, t3=None, t4=None, title=None, save_path=False
):
    fig, axs = plt.subplots(2, 2)

    plot(axs[0][0], im1, title=t1, RGB=True)
    plot(axs[0][1], im2, title=t2, RGB=True)
    plot(axs[1][0], im3, title=t3, RGB=True)
    plot(axs[1][1], im4, title=t4, RGB=True)
    fig.suptitle(title, fontsize=16)

    plt.show()
    if save_path:
        current_time = now()
        plt.savefig(rf"{save_path}/fig-{current_time}")


def show(im, save_path=False):
    plt.imshow(im, cmap="gray")
    plt.show()
    if save_path:
        current_time = now()
        plt.savefig(rf"{save_path}/fig-{current_time}")


def show2(im1, im2, t1=None, t2=None, title=None, save_path=False):
    fig, axs = plt.subplots(1, 2)

    plot(axs[0], im1, title=t1)
    plot(axs[1], im2, title=t2)

    fig.suptitle(title, fontsize=16)
    plt.show()
    if save_path:
        current_time = now()
        plt.savefig(rf"{save_path}/fig-{current_time}")


def show3(im1, im2, im3):
    f, ax = plt.subplots(1, 3)
    ax[0].imshow(im1, cmap="gray")
    ax[1].imshow(im2, cmap="gray")
    ax[2].imshow(im3, cmap="gray")
    plt.show()


def show4(
    im1,
    im2,
    im3,
    im4,
    t1=None,
    t2=None,
    t3=None,
    t4=None,
    title=None,
    save_path=False,
):
    fig, axs = plt.subplots(2, 2)

    plot(axs[0][0], im1, title=t1)
    plot(axs[0][1], im2, title=t2)
    plot(axs[1][0], im3, title=t3)
    plot(axs[1][1], im4, title=t4)

    fig.suptitle(title, fontsize=16)
    plt.show()
    if save_path:
        current_time = strftime("%H-%M-%S")
        plt.savefig(rf"{save_path}/fig-{current_time}")


def arr_det(arr):
    print(type(arr))
    print(
        f"\n shape = {arr.shape} \n dimensions = {arr.ndim} \n data type = {arr.dtype} \n size(#elements) = {arr.size} \n total memory size = {arr.size * arr.itemsize} \n max value = {arr.max()} \n min value = {arr.min()}"
    )
