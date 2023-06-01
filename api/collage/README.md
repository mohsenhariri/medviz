
# COLLAGE API

## Setup and Environment

### PIP

```bash
python -m venv yourEnvName
source yourEnvName/bin/activate
pip install --upgrade medviz
```

### Conda

Will be added soon.

## Usage

First, we need a pair of image and mask. Sometimes there exists more than one mask for an image. Sometimes there is no certain naming convention in images and masks. To get rid of these problems, we need to generate a schema for our dataset. The generated schema will be used as input for the collage and other feature extraction APIs.

1. Generate mask/annotation schema

```python

import medviz as viz

viz.match_image_mask(
        images_path="/media/storage/dataset/cropped_scans",
        masks_path="/media/storage/dataset/Annotations_Resampled",
        image_func=lambda x: x.split("_")[1],
        mask_func=lambda x: x.split("_")[1],
        save_path="pr_crohn_local/dataset_schema.csv",

    )
```

This step generates a schema for the image/masks in your dataset. The schema helps handle situations where there are multiple masks for an image or when there is no specific naming convention for images and masks. 

Optionally, you can create a spreadsheet to view the details of your masks.


``` python
from pathlib import Path
import medviz as viz

masks_path_crohn = Path("/media/storage/dataset/Annotations_Resampled")

viz.preprocess.generate_mask_schema(
    dataset_path=masks_path_crohn,
    id_func=lambda x: int(x.split("_")[1]),
    save_path="./pr_crohn_local/crohn_mask_schema.csv",
)
```

2. Compute and save collage

The next step involves using the generated schema from the previous step to compute collage features for each image/mask pair in your dataset. To accomplish this, you need to call the `generate_collage` function. This function takes the schema as input in CSV format, computes the collage features for each image, and saves them to the specified output path.

```python
import medviz as viz

viz.compute_stats_collage(
    csv_path="/home/mohsen/sync/git/mohsen/medviz/pr_crohn_local/image_masks.csv",
    stats_save_path="/home/mohsen/sync/git/mohsen/medviz/pr_crohn_local/stats",
)

```

The COLLAGE features will be saved in the `stats_save_path` directory.
