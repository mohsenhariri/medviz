from pathlib import Path

import numpy as np
import nibabel as nib

from utility import path_in


def reader(path):
    if not isinstance(path, Path):
        if isinstance(path, str):
            path = Path(path)
        else:
            raise Exception("Input must be a path.")

    path = path_in(path)

    extension = path.suffix
    print(extension)

    if extension == ".npy":
        data = np.load(path)

    if extension == ".nii" or extension == ".gz":
        data = nib.load(path).get_fdata()

    return data
