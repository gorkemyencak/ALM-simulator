import os
from pathlib import Path

def save_raw_data(df, filename: str):

    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / 'data' / 'raw'
    data_dir.mkdir(parents = True, exist_ok = True)
    
    file_path = data_dir / filename
    df.to_csv(file_path)
    print(f"{filename} saved to path {data_dir}")