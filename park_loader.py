
import pandas as pd
from pathlib import Path
import sys
import logging

def load_parks_from_csv(csv_path):
    path = Path(csv_path)
    if not path.exists():
        logging.error(f"CSV file not found: {csv_path}")
        sys.exit(1)
    df = pd.read_csv(path)
    required_cols = {'name', 'area_sqm', 'suburb'}
    if not required_cols.issubset(df.columns):
        logging.error(f"CSV missing required columns: {required_cols}")
        sys.exit(1)
    return df.to_dict(orient='records')
