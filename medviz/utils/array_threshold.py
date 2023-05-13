import numpy as np
from skimage.filters import (
    threshold_li,
    threshold_mean,
    threshold_minimum,
    threshold_otsu,
    threshold_triangle,
    threshold_yen,
)


def compute_thresholds(image):
    thresholds = {}

    thresholds["otsu"] = threshold_otsu(image)
    thresholds["li"] = threshold_li(image)
    thresholds["triangle"] = threshold_triangle(image)
    thresholds["yen"] = threshold_yen(image)
    thresholds["mean"] = threshold_mean(image)
    thresholds["minimum"] = threshold_minimum(image)
    thresholds["median"] = np.median(image)
    thresholds["min"] = np.min(image)
    thresholds["max"] = np.max(image)

    return thresholds
