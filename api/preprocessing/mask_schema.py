from pathlib import Path

import medviz as viz

masks_path_crohn_peds = Path("/media/storage/dataset/Annotations_Resampled")

viz.preprocess.generate_mask_schema(
    masks_path=masks_path_crohn_peds,
    id_func=lambda x: int(x.split("_")[1]),
    # mask_extension=".nii", # Optional
    save_path=r"./pr_crohn_local/crohn_peds_mask_schema.csv",
)


# import nibabel as nib
# p = Path("/media/storage/dataset/Annotations_Resampled/MRE_051_JM_take2_resampled.nii")

# mask = nib.load(p).get_fdata()

# a = viz.significant_slice_idx_data(mask)
# print(a)
# exit()
# viz.utils.profile([mask], unique_values=True)


# exit()
# masks_path_bowel = Path("/media/storage/github/mohsen2/bowel/results/CT_TI_nii_masks")

# masks_path_crohn_peds = "./"

# viz.preprocess.generate_mask_schema(
#     dataset_path=masks_path_bowel,
#     mask_format=".nii",
#     output_path=r"./bowel",
#     output_name="bowel_mask_schema.csv",
# )
