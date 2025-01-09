import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from typing import Tuple
import logging

logging.basicConfig(level=logging.INFO)

# Logistic Regression
def calculate_thresholds_logistic_regression(income_df: pd.DataFrame, year: str) -> Tuple[float, float]:
    income_data = income_df[year].values
    labels = pd.qcut(income_data, 3, labels=['Weak', 'Middle', 'Strong'])
    encoder = LabelEncoder()
    labels_encoded = encoder.fit_transform(labels)
    income_data_reshaped = income_data.reshape(-1, 1)

    model = LogisticRegression(random_state=42)
    model.fit(income_data_reshaped, labels_encoded)

    weak_threshold = np.percentile(income_data, 33)
    strong_threshold = np.percentile(income_data, 66)
    logging.info("Calculated economic thresholds using Logistic Regression")
    return weak_threshold, strong_threshold

# SVM Regression
def calculate_thresholds_svm(income_df: pd.DataFrame, year: str) -> Tuple[float, float]:
    income_data = income_df[year].values
    income_scaled = StandardScaler().fit_transform(income_data.reshape(-1, 1)).flatten()
    positions = np.arange(len(income_scaled))

    model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
    model.fit(positions.reshape(-1, 1), income_scaled)
    predictions = model.predict(positions.reshape(-1, 1))

    weak_threshold = np.percentile(predictions, 33)
    strong_threshold = np.percentile(predictions, 66)
    logging.info("Calculated economic thresholds using SVM Regression")
    return weak_threshold, strong_threshold

# KNN Classification
def calculate_thresholds_knn(income_df: pd.DataFrame, year: str, k: int = 3) -> Tuple[float, float]:
    income_data = income_df[year].values
    labels = pd.qcut(income_data, 3, labels=['Weak', 'Middle', 'Strong'])
    encoder = LabelEncoder()
    labels_encoded = encoder.fit_transform(labels)
    income_data_reshaped = income_data.reshape(-1, 1)

    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(income_data_reshaped, labels_encoded)

    weak_threshold = np.percentile(income_data, 33)
    strong_threshold = np.percentile(income_data, 66)
    logging.info("Calculated economic thresholds using KNN Classification")
    return weak_threshold, strong_threshold

# Main Function for Analysis
def analyze_economic_background_logistic_svm_knn(
    state: str, 
    income_df: pd.DataFrame, 
    year: str, 
    method: str = 'logistic', 
    k: int = 3
) -> str:
    if method == 'logistic':
        weak_threshold, strong_threshold = calculate_thresholds_logistic_regression(income_df, year)
    elif method == 'svm':
        weak_threshold, strong_threshold = calculate_thresholds_svm(income_df, year)
    elif method == 'knn':
        weak_threshold, strong_threshold = calculate_thresholds_knn(income_df, year, k=k)
    else:
        raise ValueError("Invalid method. Choose either 'logistic', 'svm', or 'knn'.")

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
