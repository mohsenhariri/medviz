import pandas as pd
from pathlib import Path


def filter_dicom(path_csv, series_description, save_path=None):
    df = pd.read_csv(path_csv, usecols=["Path", "SeriesDescription"])

    df = df.loc[df["SeriesDescription"].str.contains(series_description), "Path"]

    if save_path:
        save_path = Path(save_path)
        if not save_path.exists():
            save_path.mkdir(parents=True)

        save_path = save_path / Path("metadata.csv")

        df.to_csv(save_path, index=False)
    
    return df
