# MedViz

## Usage

Install the [package](https://pypi.org/project/medviz/) using `pip`:

```bash
    pip install medviz
```

Or install from the source:

```bash
    pip install git+https://github.com/mohsenhariri/medviz
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



plots

1. multiple 2D images
just images, not mask or contour

2. multiple 2D images and masks- layered plot



## 2D plots
1. 2D images.

inpute:
    - an array of images

```python
viz.plot2d_images_array()
viz.plot2d_images_path()
```

2. 2D image and masks- layered plot

inpute:
    - an image
    - an array of masks
  

```python
plot2d.image_masks()
```

## Interactive plots

1. 3D images with slider

inpute:
    - an array of images

```python
plot3d.images()
```

2. 3D images and masks- layered plot with slider

inpute:
    - an array of images
    - an array of masks
  
```python
plot3d.images_masks()
```



