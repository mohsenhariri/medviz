import medviz as viz

viz.preprocess.match_image_masks(
    images_path="/media/storage/dataset/cropped_scans_NPY",
    masks_path="/media/storage/dataset/Annotations_Resampled_NPY",
    image_id_func=lambda x: x.split("_")[1],
    mask_id_func=lambda x: x.split("_")[1],
    # save_path="./pr_crohn_local/crohn_peds_images_mask_match.csv",
)
