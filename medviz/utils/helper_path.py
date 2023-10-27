from os import getenv
from pathlib import Path
from typing import Optional

from .custom_type import PathType
from .utility import now


def path_in(path: PathType, env: bool = False) -> Path:
    """
    Converts a given path string or Path object into an absolute Path object.
    If env is set to True, it uses the ROOT_IN environment variable as a base directory.

    Parameters:
    - path (Union[str, Path]): The input path as a string or Path object.
    - env (bool, optional): Flag to indicate if the ROOT_IN environment variable
      should be used as a base directory. Defaults to False.

    Returns:
    - Path: The absolute path.

    Raises:
    - TypeError: If the input is neither a string nor a Path object.
    - FileNotFoundError: If the resulting path doesn't exist.
    """

    if isinstance(path, str):
        path = Path(path)

    if not isinstance(path, Path):
        raise TypeError(f"The input must be string or Path, not {type(path)}")

    if not path.is_absolute() and env:
        root_in = getenv("ROOT_IN") or "."
        path = Path(root_in) / path

    if not path.exists():
        raise FileNotFoundError(f"{path} doesn't exist on the earth.")

    return path


def save_path_dir(path: PathType, env: bool = False) -> Path:
    """
    Ensures the provided path string or Path object for an output directory exists.
    If the path does not exist, it creates the directory. If env is set to True,
    the ROOT_OUT environment variable is used as a base directory.

    Parameters:
    - path (Union[str, Path]): The output directory path as a string or Path object.
    - env (bool, optional): Flag to indicate if the ROOT_OUT environment variable
      should be used as a base directory. Defaults to False.

    Returns:
    - Path: The absolute path to the output directory.

    Raises:
    - TypeError: If the input is neither a string nor a Path object.
    """

    if isinstance(path, str):
        path = Path(path)

    if not isinstance(path, Path):
        raise TypeError(f"The output path must be string or Path, not {type(path)}")

    if not path.is_absolute() and env:
        root_out = getenv("ROOT_OUT") or "."
        path = Path(root_out) / path

    if not path.exists():
        print("The output path doesn't exist but no worries I'm making it.")
        path.mkdir(parents=True)

    return path


# def path_out_file(path: PathType, suffix: str or None, env: bool = False) -> Path:
#     if isinstance(path, str):
#         path = Path(path)

#     if not isinstance(path, Path):
#         raise TypeError(f"The output path must be string or Path, not {type(path)}")

#     if not path.is_absolute() and env:
#         root_out = getenv("ROOT_OUT") or "."
#         path = Path(root_out) / path

#     if not path.suffix:
#         if not suffix:
#             raise ValueError("suffix must be provided if save_path has no suffix")
#         path = path.with_suffix(suffix)

#     if not path.parent.exists():
#         print("The output path doesn't exist but no worries I'm making it.")
#         path.parent.mkdir(parents=True)

#     return path


def save_path_file(
    save_path: PathType, suffix: Optional[str] = None, env: Optional[bool] = False
) -> Path:
    """
    Generates a save path for a file, ensuring the directory exists and providing
    a suffix if necessary. If the file already exists, a timestamp is appended to
    avoid overwriting.

    Parameters:
    - save_path (PathType): The initial path (either as a string or Path object)
      where the file should be saved.
    - suffix (Optional[str], default=None): A file extension to be added if
      `save_path` lacks one. If `save_path` doesn't have a suffix and this
      parameter is not provided, a ValueError is raised.
    - env (Optional[bool], default=False): If set to True and `save_path` is not
      absolute, the function uses the ROOT_OUT environment variable as a base
      directory to construct the absolute path.

    Returns:
    - Path: The absolute path where the file should be saved.

    Raises:
    - TypeError: If `save_path` is neither a string nor a Path object.
    - ValueError: If `save_path` lacks a suffix and no suffix is provided.

    Note:
    If the computed `save_path` directory does not exist, it will be created.
    If a file already exists at the computed path, a timestamp is appended to
    the filename to ensure uniqueness.
    """

    if isinstance(save_path, str):
        save_path = Path(save_path)

    if not isinstance(save_path, Path):
        raise TypeError(f"save_path must be a str or Path, not {type(save_path)}")

    if not save_path.is_absolute() and env:
        root_out = getenv("ROOT_OUT") or "."
        save_path = Path(root_out) / save_path

    if not save_path.suffix:
        if not suffix:
            raise ValueError("suffix must be provided if save_path has no suffix")
        save_path = save_path.with_suffix(suffix)

    if not save_path.parent.exists():
        print("The output path doesn't exist but no worries I'm making it.")
        save_path.parent.mkdir(parents=True)
    elif save_path.exists():
        save_path = save_path.with_stem(save_path.stem + "_" + now())

    return save_path
