# MedViz

## Usage

Install the [package](https://pypi.org/project/medviz/) using `pip`:

```bash
    pip install medviz
```
Import the package and use the layered_plot function

```python
    import medviz

    medviz.layered_plot(image_path="dataset/1-1.nii", mask_paths=["dataset/small_bowel.nii", "dataset/1-1-label.nii"], mask_colors=["red", "yellow"], title="Layered Plot")
```

## Development

### Setup

- make env
- source env_platform_ver/bin/activate
- make
- make check
- make pireq
### Required packages

- Numpy
- Matplotlib
- Nibabel

### Slider- To do

- [x] Max
- [x] Min
- [x] Midian

1. Plot layered images and masks
2. Generate Gif



