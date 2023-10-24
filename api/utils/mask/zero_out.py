from pathlib import Path

import medviz as viz

# Mask can be in .nii, .nii.gz, .dcm, .mha, .npy, .npz formats.
multi_value_mask_path = Path(
    "/storage/sync/git/mohsen/medviz/test_local/dataset/pc/350739_CTE_AX-ng-label_Res.nii"
)

mask = viz.utils.im2arr(multi_value_mask_path)

mask_binary1 = viz.utils.zero_out(mask, 1)
mask_binary2 = viz.utils.zero_out(mask, 2)

print(viz.utils.profile([mask, mask_binary1, mask_binary2]))
