import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from typing import Tuple
import logging

logging.basicConfig(level=logging.INFO)

def calculate_thresholds_kmeans(income_df: pd.DataFrame, year: str) -> Tuple[float, float]:
    income_data = income_df[year].values.reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(income_data)
    centers = np.sort(kmeans.cluster_centers_.flatten())
    logging.info("Calculated economic thresholds using KMeans")
    return centers[0], centers[1]

def analyze_economic_background_kmeans(state: str, income_df: pd.DataFrame, year: str) -> str:
    weak_threshold, strong_threshold = calculate_thresholds_kmeans(income_df, year)
    
    state_income_series = income_df[income_df['NAME'] == state][year]
    
    if state_income_series.empty:
        logging.error(f"No income data found for state: {state}")
        return "Unknown Economic Status"  

    state_income = float(state_income_series.iloc[0])  

    if state_income < weak_threshold:
        return 'Economically Weak'
    elif weak_threshold <= state_income <= strong_threshold:
        return 'Middle Income'
    return 'Economically Strong'