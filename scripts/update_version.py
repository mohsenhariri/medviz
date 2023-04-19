import tomllib
from pathlib import Path

path = Path("pyproject.toml")

with open("VERSION", "r") as f:
    version = f.read().strip()


with path.open("rb") as fp:
    config = tomllib.load(fp, parse_float=float)

config["project"]["version"] = version
