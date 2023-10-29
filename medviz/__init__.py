# from .utils.helper_mask import *

# # from .preprocess.mask import generate_mask_schema

# from .preprocess.mask import generate_mask_schema
# from .preprocess.match_image_mask import match_image_mask

from .utils import (
    # image_path_to_data_ax,
    # image_path_to_data_sag,
    # mask_path_to_data_ax,
    # mask_path_to_data_sag,
    save_path_dir,
    save_path_file,
    path_in,
    im2arr,
    read_image_mask,
    # mask_characteristics,
)

from .plot import plot3d, gif

from .utils.array_profile import profile
from .utils.array_threshold import compute_thresholds

# from .utils import significant_slices


from .multimodal import save_dicom_metadata, filter_dicom

from .preprocess import *

from .feats import *

# from .nifti.helper import nii3d_to_annotated2d, nii_mask3d_to_2d

# def version():
#     with open("VERSION", "r") as f:
#         version = f.read().strip()
#     return version

# __version__ = version()

__version__ = "1.1.4"
