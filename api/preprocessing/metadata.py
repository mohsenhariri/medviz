### Support for metadata extraction from images
# .dcm, .nii, .nii.gz, .mha

from pathlib import Path

import medviz as viz

images = Path("/storage/sync/git/mohsen/medviz/test_local/dataset/images")

paths = list(images.glob("**/*"))

viz.metadata(paths, save_csv="export_local/metadata.csv")

## Second Use Case
# for i, path in enumerate(images.glob("**/*")):
#     print(path)
#     print(f"Suffixes: {path.suffixes}")

#     m = viz.metadata(path, save_csv=f"metadata_{i}.csv")
