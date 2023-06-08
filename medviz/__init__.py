# from .utils.helper_mask import *
# from .plots.helper_plot import *

# # from .preprocess.mask import generate_mask_schema

# # from .plots.layered_plot import *
# # from .plots.layered_plot2D import *
# # from .plots.plot_image import *
# # from .plots.plot3d.plot_images import *
# from .preprocess.mask import generate_mask_schema
# from .preprocess.match_image_mask import match_image_mask

from .utils import (
    image_path_to_data_ax,
    image_path_to_data_sag,
    mask_path_to_data_ax,
    mask_path_to_data_sag,
    save_path_dir,
    save_path_file,
    path_in,
)

from .utils.array_profile import profile
from .utils.array_threshold import compute_thresholds

### PLOT 2D ###
from .plots.plot2d.images import (
    images_array as plot2d_images_array,
    images_path as plot2d_images_path,
)

from .plots.plot2d.masks import (
    masks_array as plot2d_masks_array,
    masks_path as plot2d_masks_path,
)

from .plots.plot2d.image_masks import (
    image_masks_path as plot2d_image_masks_path,
    image_masks_array as plot2d_image_masks_array,
)


from .plots.plot2d.image_mask_annotated import (
    image_mask_annotated_array as plot2d_image_mask_annotated_array,
    image_mask_annotated_path as plot2d_image_mask_annotated_path,
)

### PLOT 3D ###


from .plots.plot3d import layered_slider_array, layered_slider_path

from .plots.plot3d.images import (
    images_array as plot3d_images_array,
    images_path as plot3d_images_path,
)

from .plots.plot3d.masks import (
    masks_array as plot3d_masks_array,
    masks_path as plot3d_masks_path,
)

from .plots.plot3d.image_masks import (
    image_masks_path as plot3d_image_masks_path,
    image_masks_array as plot3d_image_masks_array,
)

# from .plots.plot3d.layered_plot import (
#     layered_plot_data3D as plot3d_layered_data,
#     layered_plot_path3D as plot3d_layered_path,
# )

# from .plots.gif import gif, gif_slices, gif_non, gif_reference


from .multimodal import save_dicom_metadata, filter_dicom

from .preprocess import *

from .collage import compute_stats_collage

from .nifti.helper import nii3d_to_annotated2d, nii_mask3d_to_2d

# def version():
#     with open("VERSION", "r") as f:
#         version = f.read().strip()
#     return version

# __version__ = version()

__version__ = "0.9.5"
