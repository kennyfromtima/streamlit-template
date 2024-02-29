"""

    Streamlit webserver-based Social media data Extractor

    Author: Kenechukwu Ozojie.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as it suits your project needs.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from utils.profile_details import get_profile_metadata
from utils.profile_posts import get_post_metadata
from utils.profile_mentions import get_mention_metadata

# App declaration
def main():
    # building out the pages
    page_options = ["Data Extraction","Solution Overview"]

    # -------------------------------------------------------------------
    # selecting the page
    page_selection = st.sidebar.selectbox("Menu", page_options)
    if page_selection == "Data Extraction":
        # Header contents
        st.write('# TIMA Social Data Center')
        st.write('#### TIMA\'s portal for social media data sourcing')
        st.image('resources/imgs/tima_logo.png',use_column_width=True)

        # platform and data type selection
        plat = st.radio("###### Select a platform",('Instagram', 'TikTok'))
        dat = st.radio("###### Select the kind of data you need",('Profile metadata', 'Posts metadata', 'Mentions metadata'))
        # text input search bar
        text = st.text_input('###### Enter the account\'s username below',placeholder="search here...", key="text_input", value='')

        # building out the instagram and profile metadata selection
        if plat == 'Instagram' and dat == 'Profile metadata':
            if st.button("Search") or text:
                try:
                    with st.spinner('Extracting the data...'):
                        df = get_profile_metadata(text)
                    st.write(f"###### Here is {text}'s profile metadata")
                    st.write(df)

                except:
                    st.error("Oops! Looks like this account does't exist.\
                              Please cross-check the username you entered!")
        
        # building out the instagram and posts metadata selection
        if plat == 'Instagram' and dat == 'Posts metadata':
            if st.button("Search") or text:
                try:
                    with st.spinner('Extracting the data...'):
                        df = get_post_metadata(text)
                    st.write(f"###### Here is {text}'s posts metadata")
                    st.write(df)

                except:
                    st.error("Oops! Looks like this account does't exist.\
                              Please cross-check the username you entered!")
        
        # building out the instagram and mentions metadata selection
        if plat == 'Instagram' and dat == 'Mentions metadata':
            if st.button("Search") or text:
                try:
                    with st.spinner('Extracting the data...'):
                        df = get_mention_metadata(text)
                    st.write(f"###### Here is {text}'s mentions metadata")
                    st.write(df)

                except:
                    st.error("Oops! Looks like this account does't exist.\
                              Please cross-check the username you entered!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe the process of this app on this page")

    # You may want to add more sections here for other aspects such as company profile.


if __name__ == '__main__':
    main()
