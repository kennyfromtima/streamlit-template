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
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Custom Libraries
from utils.profile_details import get_profile_metadata
from utils.profile_posts import get_post_metadata
from utils.profile_mentions import get_mention_metadata
from utils.channel_details import fetch_and_aggregate_channel_data
from utils.channel_posts import fetch_videos_and_details

# App declaration
def main():
    # building out the pages
    page_options = ["Data Extraction","Data Visualization","Solution Overview"]

    # -------------------------------------------------------------------
    # selecting the page
    page_selection = st.sidebar.selectbox("Menu", page_options)
    if page_selection == "Data Extraction":
        # Header contents
        st.write('# TIMA Social Data Center')
        st.write('#### TIMA\'s portal for social media data sourcing')
        st.image('resources/imgs/tima_logo.png',use_column_width=True)

        # platform selection
        plat = st.radio("###### Select a platform",('Instagram', 'Youtube'))

        # building out the instagram selection
        if plat == 'Instagram':
            # data type selection
            dat1 = st.radio("###### Select the kind of data you need",('Profile metadata', 'Posts metadata', 'Mentions metadata'))
            # text input search bar
            text = st.text_input('###### Enter the account\'s username below',placeholder="search here...", key="text_input", value='')
            
            # building out the profile metadata selection
            if dat1 == 'Profile metadata':
                if st.button("Search") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = get_profile_metadata(text)
                        st.write(f"###### Here is {text}'s profile metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")

            # building out the posts metadata selection            
            if dat1 == 'Posts metadata':
                if st.button("Search") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = get_post_metadata(text)
                        st.write(f"###### Here is {text}'s posts metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")
                        
            # building out the mentions metadata selection
            if dat1 == 'Mentions metadata':
                if st.button("Search") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = get_mention_metadata(text)
                        st.write(f"###### Here is {text}'s mentions metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")

        # building out the youtube selection
        if plat == 'Youtube':
            # data type selection
            dat2 = st.radio("###### Select the kind of data you need",('Channel metadata', 'Posts metadata'))
            # text input search bar
            text = st.text_input('###### Enter the channel\'s ID below',placeholder="search here...", key="text_input", value='')
            
            # building out the channel metadata selection
            if dat2 == 'Channel metadata':
                if st.button("Search") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = fetch_and_aggregate_channel_data(text)
                        st.write(f"###### Here is {text}'s channel metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")
                        
            # building out the posts metadata selection
            if dat2 == 'Posts metadata':
                if st.button("Search") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = fetch_videos_and_details(text)
                        st.write(f"###### Here is {text}'s posts metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")

    # -------------------------------------------------------------------

    if page_selection == "Data Visualization":
        # Header contents
        st.write('# TIMA Social Data Center')
        st.write('#### TIMA\'s portal for social media data sourcing')
        st.image('resources/imgs/tima_logo.png',use_column_width=True)

        # platform selection
        plat = st.radio("###### Select a platform",('Instagram', 'Youtube'))

        # building out the instagram selection
        if plat == 'Instagram':
            # text input search bar
            text = st.text_input('###### Enter the account\'s username below',placeholder="search here...", key="text_input", value='')
            if st.button("Search") or text:
                try:
                    with st.spinner('Visualizing the data...'):
                        df = get_profile_metadata(text)
                    st.write(f"###### Here is {text}'s profile metadata")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Posts",df['Media Count'])
                        st.metric("Average Likes",df['Average Likes'])
                        st.metric("Images",df['Images'])
                    
                    with col2:
                        st.metric("Followers",df['Followers'])
                        st.metric("Average Comments",df['Average Comments'])
                        #st.metric("Engagement Rate",df['Engagement Rate'])
                    
                    with col3:
                        st.metric("Following",df['Following'])
                        st.metric("Average Views",df['Average Views'])
                        st.metric("Videos",df['Videos'])
                    #col1.metric("Posts",df['Media Count'])
                    #col2.metric("Followers",df['Followers'])
                    #col3.metric("Following",df['Following'])
                    #plt.pie(df['Images'])
                except:
                    st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")
        
        # building out the youtube selection
        if plat == 'Youtube':
            # text input search bar
            text = st.text_input('###### Enter the channels\'s ID below',placeholder="search here...", key="text_input", value='')
            if st.button("Search") or text:
                try:
                    with st.spinner('Visualizing the data...'):
                        df = fetch_and_aggregate_channel_data(text)
                    st.write(f"###### Here is {text}'s profile metadata")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Posts",df['Total Videos'])
                        st.metric("Average Likes",df['Average Likes per Video'])
                        #st.metric("Images",df['Images'])
                    
                    with col2:
                        st.metric("Subscribers",df['Subscriber Count'])
                        st.metric("Average Comments",df['Average Comments per Video'])
                        #st.metric("Engagement Rate",df['Engagement Rate (%)'])
                    
                    with col3:
                        st.metric("Engagement Rate",df['Engagement Rate (%)'])
                        st.metric("Average Views",df['Average Views per Video'])
                        #st.metric("Videos",df['Videos'])
                    #col1.metric("Posts",df['Media Count'])
                    #col2.metric("Followers",df['Followers'])
                    #col3.metric("Following",df['Following'])
                    #plt.pie(df['Images'])
                except:
                    st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")           
    
    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe the process of this app on this page")

    # You may want to add more sections here for other aspects such as company profile.


if __name__ == '__main__':
    main()
