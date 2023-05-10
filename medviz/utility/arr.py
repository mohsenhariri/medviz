import numpy as np
from tabulate import tabulate


def profile(arrays, unique_values=False):
    table = [
        [
            "ID",
            "Shape",
            "Dimensions",
            "Data Type",
            "Size (#Elements)",
            "Total Memory Size",
            "Max Value",
            "Min Value",
            "Sum of Values",
            "Mean Value",
            "Standard Deviation",
            "Median Value",
        ]
    ]

    if unique_values:
        table[0] += [
            "Unique Values",
            "Count of Each Unique Value",
            "Dictionary of Values and Counts",
        ]

    for i, arr in enumerate(arrays):
        row = [
            i,
            arr.shape,
            arr.ndim,
            arr.dtype,
            arr.size,
            arr.size * arr.itemsize,
            arr.max(),
            arr.min(),
            arr.sum(),
            arr.mean(),
            arr.std(),
            np.median(arr),
        ]

        if unique_values:
            unique, counts = np.unique(arr, return_counts=True)
            values = dict(zip(unique, counts))
            row += [unique, counts, values]

        table.append(row)

    print(tabulate(table, tablefmt="grid"))
