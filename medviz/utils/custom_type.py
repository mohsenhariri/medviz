from pathlib import Path
from typing import Iterable, List, Union

import numpy as np

PathType = Union[str, Path]
# example:
# path: PathType = Path("/storage/git/mohsen/medviz/dataset/1-1.nii")
# path: PathType = "/storage/git/mohsen/medviz/dataset/1-1.nii"
PathTypeLst = Union[List[Path], List[str]]
# example:
# paths: PathTypeLst = [Path("/storage/git/mohsen/medviz/dataset/1-1.nii"), Path("/storage/git/mohsen/medviz/dataset/1-1.nii")]
# paths: PathTypeLst = ["/storage/git/mohsen/medviz/dataset/1-1.nii", "/storage/git/mohsen/medviz/dataset/1-1.nii"]
PathTypeIter = Union[str, Path, Iterable[str], Iterable[Path]]
# example:
# paths: PathTypeIter = Path("/storage/git/mohsen/medviz/dataset/1-1.nii")
# paths: PathTypeIter = "/storage/git/mohsen/medviz/dataset/1-1.nii"
# paths: PathTypeIter = ["/storage/git/mohsen/medviz/dataset/1-1.nii", "/storage/git/mohsen/medviz/dataset/1-1.nii"]
# paths: PathTypeIter = [Path("/storage/git/mohsen/medviz/dataset/1-1.nii"), Path("/storage/git/mohsen/medviz/dataset/1-1.nii")]

StrLst = List[str]

NumLst = List[np.ndarray]
