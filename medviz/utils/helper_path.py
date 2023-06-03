from os import getenv
from pathlib import Path
from .utility import now


def path_in(path: str or Path, env: bool = False) -> Path:
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


def path_out_dir(path: str or Path, env: bool = False) -> Path:
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


def path_out_file(path: str or Path, suffix: str or None, env: bool = False) -> Path:
    if isinstance(path, str):
        path = Path(path)

    if not isinstance(path, Path):
        raise TypeError(f"The output path must be string or Path, not {type(path)}")

    if not path.is_absolute() and env:
        root_out = getenv("ROOT_OUT") or "."
        path = Path(root_out) / path

    if not path.suffix:
        path = path.with_suffix(suffix)

    if not path.parent.exists():
        print("The output path doesn't exist but no worries I'm making it.")
        path.parent.mkdir(parents=True)

    return path


def save_path_file(save_path: str or Path, suffix: str or None = None) -> Path:
    if isinstance(save_path, str):
        save_path = Path(save_path)

    if not isinstance(save_path, Path):
        raise TypeError(f"save_path must be a str or Path, not {type(save_path)}")

    if not save_path.suffix:
        save_path = save_path.with_suffix(suffix)

    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True)
    elif save_path.exists():
        save_path = save_path.with_stem(save_path.stem + "_" + now())

    return save_path


def save_path_dir(save_path: str or Path) -> Path:
    if isinstance(save_path, str):
        save_path = Path(save_path)

    if not isinstance(save_path, Path):
        raise TypeError(f"save_path must be a STRING or PATH, not {type(save_path)}")

    if not save_path.exists():
        save_path.mkdir(parents=True)

    return save_path
