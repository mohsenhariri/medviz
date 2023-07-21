from pathlib import Path

import medviz as viz

masks_path_crohn_peds = Path("/media/storage/dataset/Annotations_Resampled")


mask_paths = masks_path_crohn_peds.glob("*.nii")

for mask_path in mask_paths:
    mask_arr = viz.mask_path_to_data_ax(mask_path)
    print(viz.utils.profile([mask_arr]))
    break
