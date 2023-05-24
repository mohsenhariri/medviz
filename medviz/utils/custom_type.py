from pathlib import Path
from typing import Iterable, Union

PathTypeIter = Union[str, Path, Iterable[str], Iterable[Path]]
PathType = Union[str, Path]
