import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)

def preprocess_nutrition_data(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the nutritional dataset."""
    return data.dropna().reset_index()
