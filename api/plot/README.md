# Plotting

## 3D plots
1. Basic Usage:
Plot a single image without any mask:

```python
    viz.plot3d('path/to/image.nii')
```

2. Plotting Multiple Images:
If you have multiple images to plot:

```python
    images = ['path/to/image1.nii', 'path/to/image2.nii']
    viz.plot3d(images)
```

3. Displaying Images with Masks:
To visualize images along with their corresponding masks:

```python
    images = ['path/to/image1.nii', 'path/to/image2.nii']
    masks = ['path/to/mask1.nii', 'path/to/mask2.nii']
    viz.plot3d(images, masks=masks)
```

4. Using Custom Colors:
To specify custom colors for the masks:

```python
    images = ['path/to/image1.nii', 'path/to/image2.nii']
    masks = ['path/to/mask1.nii', 'path/to/mask2.nii']
    colors = ['red', 'green']
    viz.plot3d(images, masks=masks, colors=colors)
```

5. Displaying Titles:
For adding titles to the plotted images:

```python
    images = ['path/to/image1.nii', 'path/to/image2.nii']
    masks = ['path/to/mask1.nii', 'path/to/mask2.nii']
    colors = ['red', 'green']
    titles = ['Image 1', 'Image 2']
    viz.plot3d(images, masks=masks, colors=colors, titles=titles)
```

6. Specifying Display Plane:
You can visualize the images in different planes:

```python
    viz.plot3d('path/to/image.nii', plane="sagittal")
```

7. Saving the Plot:
To save the plot to a specified location:

```python
    viz.plot3d('path/to/image.nii', save_path='path/to/save_directory/')
```

8. Specifying Rows and Columns:
To organize multiple images into a specific number of rows and columns:

Specify Rows:
```python
    images = ['path/to/image1.nii', 'path/to/image2.nii', 'path/to/image3.nii']
    viz.plot3d(images, rows=2)
```

This will generate a 2x2 grid, with the third image in the first cell of the second row.

Specify Columns:
```python
    images = ['path/to/image1.nii', 'path/to/image2.nii', 'path/to/image3.nii']
    viz.plot3d(images, columns=2)
```

This will also generate a 2x2 grid similar to the previous example.

Specifying Both Rows and Columns:
For more control, you can specify both rows and columns:

```python
    images = ['path/to/image1.nii', 'path/to/image2.nii', 'path/to/image3.nii', 'path/to/image4.nii']
    viz.plot3d(images, rows=2, columns=2)
```
This will arrange the images in a 2x2 grid with each cell having one image.

9. Combining Multiple Options:
You can also combine multiple options for a comprehensive view:

```python
    images = ['path/to/image1.nii', 'path/to/image2.nii']
    masks = ['path/to/mask1.nii', 'path/to/mask2.nii']
    titles = ["First Image with Mask", "Second Image with Mask"]
    mask_colors = ["#FF0000", "#00FF00"]
    viz.plot3d(images, masks=masks, mask_colors=mask_colors, titles=titles, save_path='path/to/save_directory/')
```


