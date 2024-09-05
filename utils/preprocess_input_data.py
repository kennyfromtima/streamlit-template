"""

    Helper functions for preprocessing
    data before model predictions

    Author: Kenechukwu Ozojie.

"""
# import required libraries
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Preprocessing function
@st.cache_data(ttl=10800, show_spinner=False)
def preprocess_df(data, new_data):
    # Drop unnecessary columns
    data = data.drop(columns=['Description', 'Hashtags', 'URL', 'Date Posted'])

    # Add the new data as the last row
    data = pd.concat([data, pd.DataFrame(new_data, index=[0])], ignore_index=True)

    # Handle missing values by filling with 'None' for object columns, or mean for numeric columns
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].fillna('None')
    
    for col in data.select_dtypes(include=[np.number]).columns:
        data[col] = data[col].fillna(data[col].mean())

    # Label Encoding for categorical variables
    label_encoders = {}
    categorical_cols = ['Title', 'YouTube Short', 'Weekday']
    
    for col in categorical_cols:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

    # Standardize numeric features
    scaler = StandardScaler()
    data[['Likes', 'Comments', 'Engagement Rate', 'Video Duration in Seconds', 'Hour of Day']] = scaler.fit_transform(
        data[['Likes', 'Comments', 'Engagement Rate', 'Video Duration in Seconds', 'Hour of Day']]
    )
    
    return data