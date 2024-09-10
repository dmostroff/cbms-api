from pathlib import Path
import errno
import os
import pandas as pd

def csv_to_df( filename: str) -> pd.DataFrame:
    df = None
    fpath =  Path( filename)
    if fpath.exists():
        df = pd.read_csv(filename, sep='\t', header=0)
        # df = pd.read_csv(filename, sep='\t', header=0, nrows=chunk_size, skiprows=total_rows)
    else:
        raise FileNotFoundError( errno.ENOENT, os.strerror( errno.ENOENT), filename)
    return df
