"""

    Helper functions for preprocessing
    data before model predictions

    Author: Kenechukwu Ozojie.

"""
# import required libraries
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler

# define the function
@st.cache_data(ttl=10800, show_spinner=False)
def preprocess_data(df):
    # Isolate the 'Date Posted' and 'Views' columns
    df = df[['Date Posted', 'Views']]

    # Convert 'Date Posted' to datetime format
    df['Date Posted'] = pd.to_datetime(df['Date Posted'])

    # Rename 'Date Posted' to 'date' and set it as the index
    df.rename(columns={'Date Posted': 'date'}, inplace=True)
    df.set_index('date', inplace=True)

    # Aggregate Views by month
    df_monthly = df['Views'].resample('ME').sum()

    # Create lag features (e.g., lag 1, lag 2, ...)
    def create_lag_features(data, lags=6):
        df = pd.DataFrame(data)
        columns = [df.shift(i) for i in range(1, lags + 1)]
        columns.append(df)
        df = pd.concat(columns, axis=1)
        df.columns = ['lag_{}'.format(i) for i in range(lags, 0, -1)] + ['target']
        df.dropna(inplace=True)
        return df

    # Create lag features
    lags = 6  # Number of previous months to use as features
    df_lagged = create_lag_features(df_monthly, lags)

    # Scaling the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_lagged.drop('target', axis=1))
    
    return X_scaled, df_monthly