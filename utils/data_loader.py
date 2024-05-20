"""

    Helper functions for data loading and manipulation.

    Author: Kenechukwu Ozojie.

"""
# Data handling dependencies
import pandas as pd
import numpy as np

def load_data(path_to_data):
    """Load data from provided source.

    Parameters
    ----------
    path_to_data : str
        Relative or absolute path to the data stored
        in .csv format.

    Returns
    -------
    list[str]
        data.

    """
    df = pd.read_csv(path_to_data)
    df = df.dropna()
    data = df['title'].to_list()
    return data
