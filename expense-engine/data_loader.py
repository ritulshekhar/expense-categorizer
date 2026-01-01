import pandas as pd

def load_csv(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower()
    return df