############################################################# APP DEPENDENCIES ###################################################################
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
from streamlit_option_menu import option_menu

# Data handling dependencies
import datetime
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
from linkedin_api import Linkedin
import pygwalker as pyg
import pandas as pd
import numpy as np

# Custom Libraries
from utils.profile_details import get_profile_metadata
from utils.profile_posts import get_post_metadata
from utils.profile_mentions import get_mention_metadata
from utils.channel_details import fetch_and_aggregate_channel_data
from utils.channel_posts import fetch_videos_and_details
from utils.artist_details import get_artist_data
from utils.podcast_details import get_podcast_data
############################################################# APP CONFIGURATION PAGE ###################################################################
# Set the page config
st.set_page_config(page_title="TIMA Social Data Center", page_icon="📊")

# App declaration
def main():
    # Custom CSS
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        color: black;
    }
    .sidebar .sidebar-content h2 {
        color: #007bff;
    }
    .stButton>button {
        background-color: #FA040F;
        color: white;
        border-radius: 8px;
        padding: 0.3em;
    }
    .stButton>button:hover {
        color: white;
        background-color: #808B96;
    }
    .stRadio>label {
        font-size: 1.1em;
        color: #007bff;
    }
    .stTextInput>label {
        font-size: 1.1em;
        color: #007bff;
    }
    .stSpinner>div>div {
        border-color: #007bff transparent #007bff transparent;
    }
    </style>
    """, unsafe_allow_html=True)

    # building out the pages
    page_options = ["Data Extraction","Data Visualization","Competitors' Insight","Solution Overview"]

    # Sidebar menu
    with st.sidebar:
        st.image('resources/imgs/tima_logo.png', use_column_width=True)
        st.markdown("<h2 style='text-align: center;'>TIMA Social Data Center</h2>", unsafe_allow_html=True)
        page_selection = option_menu(" ", page_options,
                                     icons=["cloud-download", "bar-chart-line", "shield-shaded", "lightbulb"],
                                     menu_icon="cast", default_index=0, orientation="vertical",
                                     styles={"container": {"padding": "0!important", "background-color": "black"},
                                             "icon": {"color": "#007bff", "font-size": "23px"},
                                             "nav-link": {"font-size": "17px", "text-align": "center", "margin": "0px", "--hover-color": "#808B96"},
                                             "nav-link-selected": {"background-color": "#FA040F", "color": "white"}})
############################################################# DATA EXTRACTION PAGE ###################################################################
    # selecting the page
    if page_selection == "Data Extraction":
        # Header contents
        st.image('resources/imgs/tima_logo.png',use_column_width=True,)
        st.markdown("<h3 style='text-align: center; color: #007bff;'>📤 Data Extraction</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: grey; font-style: italic'>TIMA\'s portal for social media data sourcing 📊</h5>", unsafe_allow_html=True)
        st.markdown('---')

        # creating columns
        col1, col2 = st.columns(2)

        with col1:
            # platform selection
            plat = st.radio("##### Select a platform",('🎦 Youtube', '📸 Instagram', '🎧 Spotify', '👔 Linkedin'))
    
        # building out the instagram selection
        if plat == '📸 Instagram':
            with col2:
                # data type selection
                dat1 = st.radio("##### Select the kind of data you need",('🙎🏻‍♂️ Profile `metadata`', '💌 Posts `metadata`', '📢 Mentions `metadata`'))
            st.markdown('---')

            # text input search bar
            text = st.text_input('###### Enter the account\'s username below 👇',placeholder="search here...", key="text_input", value='')
            
            # building out the profile metadata selection
            if dat1 == '🙎🏻‍♂️ Profile `metadata`':
                if st.button("⏬ Extract") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = get_profile_metadata(text)

                        st.write(f"###### Here is {text}'s profile metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")

            # building out the posts metadata selection            
            if dat1 == '💌 Posts `metadata`':
                if st.button("⏬ Extract") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = get_post_metadata(text)

                        st.write(f"###### Here is {text}'s posts metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")
                        
            # building out the mentions metadata selection
            if dat1 == '📢 Mentions `metadata`':
                if st.button("⏬ Extract") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = get_mention_metadata(text)

                        st.write(f"###### Here is {text}'s mentions metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")

        # building out the youtube selection
        if plat == '🎦 Youtube':
            with col2:
                # data type selection
                dat2 = st.radio("##### Select the kind of data you need",('📺 Channel `metadata`', '🎬 Posts `metadata`'))
            st.markdown('---')

            # text input search bar
            text = st.text_input('###### Enter the channel\'s username below 👇',placeholder="search here...", key="text_input", value='')
            
            # building out the channel metadata selection
            if dat2 == '📺 Channel `metadata`':
                if st.button("⏬ Extract") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df, error_message, profile_pic_url = fetch_and_aggregate_channel_data(text)
                        if error_message:
                            st.write(error_message)
                        else:
                            st.write(f"###### Here is {text}'s channel metadata")
                            st.image(profile_pic_url, caption='@'+text)
                            st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")
                        
            # building out the posts metadata selection
            if dat2 == '🎬 Posts `metadata`':
                if st.button("⏬ Extract") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            df = fetch_videos_and_details(text)

                        st.write(f"###### Here is {text}'s posts metadata")
                        st.dataframe(df)

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")

        # building out the spotify selection
        if plat == '🎧 Spotify':
            with col2:
                # data type selection
                dat2 = st.radio("##### Select the kind of data you need",('👨‍🎤 Artist `metadata`', '🎙️ Podcast `metadata`'))
            st.markdown('---')

            # text input search bar
            text = st.text_input('###### Enter the account\'s username below 👇',placeholder="search here...", key="text_input", value='')
            
            # building out the artist metadata selection
            if dat2 == '👨‍🎤 Artist `metadata`':
                if st.button("⏬ Extract") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            result = get_artist_data(text)
                        if result:
                            artist_df, top_tracks_df, image_url = result
                            if not artist_df.empty:
                                st.write(f"###### Here is {text}'s profile metadata")
                                if image_url:
                                    st.image(image_url, caption=f'@{text}', width=100)
                                st.dataframe(artist_df)
                            if not top_tracks_df.empty:
                                st.write(f"###### Here are {text}'s top songs")
                                st.dataframe(top_tracks_df)
                        else:
                            print("Failed to retrieve data.")

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")
                        
            # building out the podcast metadata selection
            if dat2 == '🎙️ Podcast `metadata`':
                if st.button("⏬ Extract") or text:
                    try:
                        with st.spinner('Extracting the data...'):
                            result = get_podcast_data(text)
                        if result:
                            podcast_df, episodes_df = result
                            name = podcast_df['Podcast Name'][0]
                            if not podcast_df.empty:
                                st.write(f"###### Here is {name}'s profile metadata")
                                if podcast_df['Image URL'][0] != 'N/A':
                                    st.image(podcast_df['Image URL'][0], caption=f'@{name}', width=100)
                                st.dataframe(podcast_df)
                            if not episodes_df.empty:
                                st.write(f"###### Here are {name}'s recent episodes")
                                st.dataframe(episodes_df)
                        else:
                            print("Failed to retrieve data.")

                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                Please cross-check your network connection and the username you entered!")
        #---------------------------------------------------------------------------------------------------------------------------            
        # building out the linkedin selection
        if plat == '👔 Linkedin':
            with col2:
                # setup a log in area for Linkedin
                st.write("##### Log in to your Linkedin account to access Linkedin's API")
                user = st.text_input('###### Username(Email)',placeholder="type here...")
                passw = st.text_input('###### Password',placeholder="type here...", type='password')

                st.write("##### Specify the target account 👇")
                target = st.text_input('###### Username',placeholder="type here...")
                login = st.button("🔐 Get data")

            # Create logic for data extraction
            if user and passw and target and login:
                try:
                    with col2:
                        with st.spinner('Fetching data...'):
                            api = Linkedin(username=user, password=passw)
                            # Fetch the target user's profile data
                            profile = api.get_profile(target)
                                
                    st.toast("Successful", icon='✅')
                    st.markdown('---')

                    with st.spinner('Compiling data...'):

                        #------------------------------------------------------------------------------------------
                        # Definition of an Important Function
                        # Function to extract an account's Linkedin info
                        @st.cache_data(ttl=10800, show_spinner=False)
                        def extract_essential_info(profile):
                            # Extract profile picture URL
                            profile_picture_url = profile.get("displayPictureUrl", "")

                            essential_info = {
                                "Full Name": f"{profile.get('firstName', '')} {profile.get('lastName', '')}",
                                "Headline": profile.get("headline", ""),
                                "Location": profile.get("locationName", ""),
                                "Industry": profile.get("industryName", ""),
                                "Current Position": profile.get("headline", ""),
                                "Current Company": profile.get("companyName", ""),
                                "Skills": [skill["name"] for skill in profile.get("skills", [])],
                                "Number of Connections": profile.get("connections", 0),  # Adjusted field name
                                "Number of Followers": profile.get("followerCount", 0),  # Adjusted field name
                                "Profile Picture URL": profile_picture_url
                            }
                            return essential_info
                        # --------------------------------------------------------------------------------------------
                            
                        # Extract and display the essential information
                        essential_profile = extract_essential_info(profile)

                        st.subheader(f"Essential Profile Data for {target}")
                        for key, value in essential_profile.items():
                            if key == "Skills":
                                st.subheader(key)
                                for item in value:
                                    st.write(f"  - {item}")
                            else:
                                st.subheader(key)
                                st.write(value)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        #------------------------------------------------------------------------------------------------------------------------
############################################################# DATA VISUALIZATION PAGE ###################################################################
    # Function to format numbers to nearest thousand with 'K'
    def format_number(num):
        if num < 1000:
            return str(num)
        elif 1000 <= num < 1000000:
            return f"{num/1000:.1f}K"
        else:
            return f"{num/1000000:.2f}M"

    if page_selection == "Data Visualization":
        # Header contents
        st.image('resources/imgs/tima_logo.png',use_column_width=True,)
        st.markdown("<h3 style='text-align: center; color: #FA040F;'>📈 Data Visualization</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: grey; font-style: italic'>TIMA\'s portal for social media data sourcing 📊</h5>", unsafe_allow_html=True)
        st.markdown('---')

        col3, col4 = st.columns(2)
        with col3:
            plat = st.radio("##### Select a platform",('🎦 Youtube', '📸 Instagram'))

        # logic control for instagram
        if plat == '📸 Instagram':
            with col4:
                # platform selection
                viz = st.radio("##### Select Visualization type",options=('🤖 Get `ready-made` visuals', '🛠️ Get `custom-made` visuals'))
            st.markdown('---')

            # building out the ready-made selection
            if viz == '🤖 Get `ready-made` visuals':
                # text input search bar
                text = st.text_input('###### Enter the account\'s username below 👇',placeholder="search here...", key="text_input", value='')
                if st.button("⏩ Visualize") or text:
                    # try extracting the profile metadata
                    try:
                        with st.spinner('Visualizing the data...'):
                            # Fetch the data
                            df = get_profile_metadata(text)

                        # Use the username in the output
                        st.write(f"Here is {text}'s profile metadata", unsafe_allow_html=True)

                        # Display Profile Picture prominently
                        #st.image(df['Profile Pic'].iloc[0], width=200, caption=f"{text}'s Profile Picture", use_column_width=False)

                        # Adjusted layout for profile metrics
                        col5, col6, col7, col8 = st.columns([3, 1, 1, 1])
                        
                        with col5:
                            st.markdown("""<style>.font {font-size:14px;}</style>""", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Username:</b> {df['User Name'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Full Name:</b> {df['Full Name'].iloc[0] if df['Full Name'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Biography:</b> {df['Biography'].iloc[0][:300] + '...' if len(df['Biography'].iloc[0]) > 300 else df['Biography'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Profile URL:</b> <a href='{df['Profile URL'].iloc[0]}' target='_blank'>{df['Profile URL'].iloc[0]}</a></div>", unsafe_allow_html=True)

                        with col6:
                            formatted_followers = format_number(df['Followers'].iloc[0])
                            st.metric("Followers", formatted_followers)
                            formatted_following = format_number(df['Following'].iloc[0])
                            st.metric("Following", formatted_following)
                        
                        with col7:
                            formatted_posts = format_number(df['Media Count'].iloc[0])
                            st.metric("Total Posts", formatted_posts)  

                        # Metrics and pie chart in a new row
                        col9, col10, col11, col12, col_space, col13 = st.columns([4, 4, 4, 4, 1, 4])

                        metrics_style = "<style>.metrics {font-size:18px; font-weight:bold; color:white;} .submetrics {font-size:17px; color:grey;}</style>"

                        with col9:
                            total_likes = "{:,}".format(df['Total Likes'].iloc[0])
                            avg_likes = "{:,}".format(df['Average Likes'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Number of Likes</div><div class='submetrics'>{total_likes}<br>Average: {avg_likes}</div>", unsafe_allow_html=True)

                        with col10:
                            engagement_rate = "{:}".format(df['Engagement Rate'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Engagement Rate</div><div class='submetrics'>{engagement_rate}</div>", unsafe_allow_html=True)
                            estimated_reach = "{:,}".format(df['Estimated Reach'].iloc[0]) 
                            st.markdown(metrics_style + f"<div class='metrics'>Est. Reach</div><div class='submetrics'>{estimated_reach}</div>", unsafe_allow_html=True)

                        with col11:
                            total_comments = "{:,}".format(df['Total Comments'].iloc[0])
                            avg_comments = "{:,}".format(df['Average Comments'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Number of Comments</div><div class='submetrics'>{total_comments}<br>Average: {avg_comments}</div>", unsafe_allow_html=True)

                        with col12:
                            total_views = "{:,}".format(df['Total Views'].iloc[0])
                            avg_views = "{:,}".format(df['Average Views'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Number of Views</div><div class='submetrics'>{total_views}<br>Average: {avg_views}</div>", unsafe_allow_html=True)

                        # Pie chart for videos vs photos
                        #with col13:
                            #labels = ['Videos', 'Images']
                            #values = [df['Videos'].iloc[0], df['Images'].iloc[0]]
                            #fig = px.pie(names=labels, values=values, title="Videos vs Images Distribution")
                            #fig.update_traces(textinfo='value+percent', pull=[0.1, 0])
                            #fig.update_layout(width=300, height=400)  # Adjust the size as needed
                            #st.plotly_chart(fig)

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                    except:
                        st.error("Oops! Looks like this account doesn't exist, or there is a network error. Please cross-check your network connection and the username you entered!")


                    # try extracting the post metadata
                    try:
                        with st.spinner('Visualizing more data...'):
                            # Fetch the data
                            df_posts = get_post_metadata(text)
                        
                        # Normalize the 'Hashtags' column to ensure each row contains a list
                        df_posts['Hashtags'] = df_posts['Hashtags'].apply(lambda x: x if isinstance(x, list) else [x] if isinstance(x, str) else [])
                        
                        # Concatenate all hashtags into a single list
                        all_hashtags_list = sum(df_posts['Hashtags'].tolist(), [])
                        
                        # Join all hashtags in the list into a single string separated by spaces
                        all_hashtags_string = ' '.join(all_hashtags_list)

                        # display the table
                        st.write("### Trending Posts")
                        df_filtered = df_posts[['Date', 'Post Type', 'Likes', 'Comments', 'Video Views', 'Post URL']]
                        st.dataframe(df_filtered, height=400)

                        # Generate the Word Cloud with adjusted parameters
                        wordcloud = WordCloud(
                            background_color='white',
                            max_words=200,
                            min_word_length=4,
                            width=2000,
                            height=1000
                        ).generate(all_hashtags_string)


                        # Display Word Cloud visual
                        st.write("### Trending Hashtags")
                        fig, ax = plt.subplots()
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)

                        # Ensure 'Date' is a datetime object and extract the year, month
                        df_posts['Date'] = pd.to_datetime(df_posts['Date'])
                        df_posts['Year'] = df_posts['Date'].dt.year
                        df_posts['Month'] = df_posts['Date'].dt.strftime('%B %Y')

                        # Filter the DataFrame to include only the past 5 years
                        current_year = pd.to_datetime('today').year
                        df_filtered = df_posts[df_posts['Year'] >= current_year - 5]

                        # Aggregate likes, comments, and views by year
                        aggregated_data = df_filtered.groupby('Year').agg({
                            'Likes': 'sum',
                            'Comments': 'sum',
                            'Video Views': 'sum'
                        }).reset_index()
                        
                        # Generate and display interactive bar charts
                        # Likes History
                        fig_likes = px.bar(aggregated_data, x='Year', y='Likes', title='Likes History Over the Past 5 Years', 
                                        text='Likes', color_discrete_sequence=["#636EFA"])
                        fig_likes.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Likes")
                        fig_likes.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                        
                        # Comments History
                        fig_comments = px.bar(aggregated_data, x='Year', y='Comments', title='Comments History Over the Past 5 Years', 
                                            text='Comments', color_discrete_sequence=["#EF553B"])
                        fig_comments.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Comments")
                        fig_comments.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                        
                        # Views History
                        fig_views = px.bar(aggregated_data, x='Year', y='Video Views', title='Views History Over the Past 5 Years', 
                                        text='Video Views', color_discrete_sequence=["#00CC96"])
                        fig_views.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Video Views")
                        fig_views.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                        
                        # Display the bar charts
                        st.plotly_chart(fig_likes, use_container_width=True)
                        st.plotly_chart(fig_comments, use_container_width=True)
                        st.plotly_chart(fig_views, use_container_width=True)
                    
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

                    # try extracting the mentions metadata
                    try:
                        with st.spinner('Visualizing more data...'):
                            # Fetch the data
                            df_mentions = get_mention_metadata(text)
                    
                        # Displaying a message to indicate data fetching is done
                        st.success('Data fetched successfully!')
                        
                        # Renaming and selecting specific columns for the display as per requirements
                        df_display = df_mentions[['Date', 'User Id', 'Post Type', 'Likes', 'Comments', 'Post URL']]
                        
                        # Setting the column names as needed
                        df_display.columns = ['Date', 'User ID', 'Post Type', 'Likes', 'Comments', 'URL']
                        
                        # Display the table as scrollable, adjusting height to show about 10 rows
                        st.write("### Trending Mentions")
                        st.dataframe(df_display, height=400)  # Adjust the height as needed to fit 10 rows visibly
                    
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            
            # building out the custom-made selection
            if viz == '🛠️ Get `custom-made` visuals':
                # text input search bar
                text2 = st.text_input('###### Enter the account\'s username below 👇',placeholder="search here...", key="text_input", value='')
                if st.button("⏩ Visualize") or text2:
                    # try extracting the profile metadata
                    try:
                        with st.spinner('Visualizing the data...'):
                            df = get_profile_metadata(text2)

                        # Generate the HTML using Pygwalker
                        pyg_html = pyg.to_html(df)

                        # Embed the HTML into the Streamlit app
                        st.write(f"###### Here is {text2}'s profile metadata")
                        components.html(pyg_html, height=1000, width=1000, scrolling=True)

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                    Please cross-check your network connection and the username you entered!")           

                    # try extracting the post metadata
                    try:
                        with st.spinner('Visualizing more data...'):
                            df2 = get_post_metadata(text2)

                        # Generate the HTML using Pygwalker
                        pyg_html2 = pyg.to_html(df2)
    
                        # Embed the HTML into the Streamlit app
                        st.write(f"###### Here is {text2}'s posts metadata")
                        components.html(pyg_html2, height=1000, width=1000, scrolling=True)
                    
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

                    # try extracting the mentions metadata
                    try:
                        with st.spinner('Visualizing more data...'):
                            df3 = get_mention_metadata(text2)

                        # Generate the HTML using Pygwalker
                        pyg_html3 = pyg.to_html(df3)
    
                        # Embed the HTML into the Streamlit app
                        st.write(f"###### Here is {text2}'s mentions metadata")
                        components.html(pyg_html3, height=1000, width=1000, scrolling=True)
                    
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

        # logic control for youtube
        if plat == '🎦 Youtube':
            with col4:
                # platform selection
                viz = st.radio("##### Select Visualization type",options=('🤖 Get `ready-made` visuals', '🛠️ Get `custom-made` visuals'))
            st.markdown('---')

            # building out the ready-made selection
            if viz == '🤖 Get `ready-made` visuals':
                # text input search bar
                text = st.text_input('###### Enter the channels\'s username below 👇',placeholder="search here...", key="text_input", value='')
                if st.button("⏩ Visualize") or text:
                    # try extracting the channel metadata
                    try:
                        with st.spinner('Visualizing the data...'):
                            df, error_message, profile_pic_url = fetch_and_aggregate_channel_data(text)
                        if error_message:
                            st.write(error_message)

                        # Use the username in the output
                        st.write(f"Here is {text}'s profile metadata", unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)

                        # Adjusted layout for profile metrics
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        
                        with col1:
                            st.image(profile_pic_url, caption='@'+text)
                            st.markdown("""<style>.font {font-size:14px;}</style>""", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Username:</b> {df['Title'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>About:</b> {df['Description'].iloc[0] if df['Description'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Country:</b> {df['Country'].iloc[0] if df['Country'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Channel URL:</b> <a href='{df['Channel URL'].iloc[0]}' target='_blank'>{df['Channel URL'].iloc[0]}</a></div>", unsafe_allow_html=True)

                        with col2:
                            formatted_followers = format_number(df['Subscriber Count'].iloc[0])
                            st.metric("Subscribers", formatted_followers)
                            
                        
                        with col3:
                            formatted_posts = format_number(df['Total Videos'].iloc[0])
                            st.metric("Total Videos", formatted_posts)

                        
                        col5, col6, col7, col8, col_space, col9 = st.columns([4, 4, 4, 4, 1, 4])

                        metrics_style = "<style>.metrics {font-size:18px; font-weight:bold; color:white;} .submetrics {font-size:17px; color:grey;}</style>"

                        with col5:
                            total_likes = "{:,}".format(df['Total Likes'].iloc[0])
                            avg_likes = "{:,}".format(df['Average Likes per Video'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Number of Likes</div><div class='submetrics'>{total_likes}<br>Average: {avg_likes}</div>", unsafe_allow_html=True)

                        with col6:
                            engagement_rate = "{:.2f}".format(df['Engagement Rate (%)'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Engagement Rate %</div><div class='submetrics'>{engagement_rate}</div>", unsafe_allow_html=True)
                            estimated_reach = "{:,}".format(df['Estimated Reach'].iloc[0])  
                            st.markdown(metrics_style + f"<div class='metrics'>Est. Reach</div><div class='submetrics'>{estimated_reach}</div>", unsafe_allow_html=True)

                        with col7:
                            total_comments = "{:,}".format(df['Total Comments'].iloc[0])
                            avg_comments = "{:,}".format(df['Average Comments per Video'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Number of Comments</div><div class='submetrics'>{total_comments}<br>Average: {avg_comments}</div>", unsafe_allow_html=True)

                        with col8:
                            total_views = "{:,}".format(df['Total Views'].iloc[0])
                            avg_views = "{:,}".format(df['Average Views per Video'].iloc[0])
                            st.markdown(metrics_style + f"<div class='metrics'>Number of Views</div><div class='submetrics'>{total_views}<br>Average: {avg_views}</div>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                    
                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                    Please cross-check your network connection and the username you entered!")
                    
                    # try extracting the posts metadata
                    try:
                        with st.spinner('Visualizing more data...'):
                            df = fetch_videos_and_details(text) 
                        # Ensure 'Date' is a datetime object and extract the year
                        df['Date Posted'] = pd.to_datetime(df['Date Posted'])
                        df['Year'] = df['Date Posted'].dt.year

                        # Filter the DataFrame to include only the past 5 years
                        current_year = pd.to_datetime('today').year
                        df_filtered = df[df['Year'] >= current_year - 5]

                        # Aggregate likes, comments, and views by year
                        aggregated_data = df_filtered.groupby('Year').agg({
                            'Likes': 'sum',
                            'Comments': 'sum',
                            'Views': 'sum'
                        }).reset_index()
                    
                        # Plotting the bar charts
                        fig_likes = px.bar(aggregated_data, x='Year', y='Likes', title='Likes History Over the Past 5 Years',
                                            color_discrete_sequence=["#636EFA"])
                        fig_comments = px.bar(aggregated_data, x='Year', y='Comments', title='Comments History Over the Past 5 Years',
                                                color_discrete_sequence=["#EF553B"])
                        fig_views = px.bar(aggregated_data, x='Year', y='Views', title='Views History Over the Past 5 Years',
                                            color_discrete_sequence=["#00CC96"])

                        st.plotly_chart(fig_likes, use_container_width=True)
                        st.plotly_chart(fig_comments, use_container_width=True)
                        st.plotly_chart(fig_views, use_container_width=True)
                
                        #Setting up a Table for posts
                        # Renaming and selecting specific columns for the display as per requirements
                        df_display = df[['Title', 'Date Posted', 'Description', 'Views', 'Likes', 'Comments', 'URL']]
                        
                        # Setting the column names as needed
                        df_display.columns = ['Title', 'Date', 'Description', 'Views', 'Likes', 'Comments', 'URL']
                        
                        # Display the table as scrollable, adjusting height to show about 10 rows
                        st.write("### Channel Posts")
                        st.dataframe(df_display, height=400)  # Adjust the height as needed to fit 10 rows visibly
                    
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            
            # building out the custom-made selection
            if viz == '🛠️ Get `custom-made` visuals':
                # text input search bar
                text2 = st.text_input('###### Enter the channels\'s username below 👇',placeholder="search here...", key="text_input", value='')
                if st.button("⏩ Visualize") or text2:
                    # try extracting the channel metadata
                    try:
                        with st.spinner('Visualizing the data...'):
                            df, error_message, profile_pic_url = fetch_and_aggregate_channel_data(text2)
                        if error_message:
                            st.write(error_message)

                        # Generate the HTML using Pygwalker
                        pyg_html = pyg.to_html(df)
    
                        # Embed the HTML into the Streamlit app
                        st.write(f"###### Here is {text2}'s profile metadata", unsafe_allow_html=True)
                        st.image(profile_pic_url, caption='@'+text2)
                        components.html(pyg_html, height=1000, width=1000, scrolling=True)

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                    except:
                        st.error("Oops! Looks like this account does't exist, or there is a network error.\
                                    Please cross-check your network connection and the username you entered!")
                    
                    # try extracting the posts metadata
                    try:
                        with st.spinner('Visualizing more data...'):
                            df2 = fetch_videos_and_details(text2)

                        # Generate the HTML using Pygwalker
                        pyg_html2 = pyg.to_html(df2)
    
                        # Embed the HTML into the Streamlit app
                        st.write(f"###### Here is {text2}'s posts metadata")
                        components.html(pyg_html2, height=1000, width=1000, scrolling=True)

                    except Exception as e:
                        st.error(f"An error occurred: {e}") 
############################################################# COMPETITORS' INSIGHT PAGE ###################################################################

    if page_selection == "Competitors' Insight":
        # Header contents
        st.image('resources/imgs/tima_logo.png',use_column_width=True,)
        st.markdown("<h3 style='text-align: center; color: #F4D03F;'>🛡️ Competitors' Insight</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: grey; font-style: italic'>TIMA\'s portal for social media data sourcing 📊</h5>", unsafe_allow_html=True)
        st.markdown('---')
        st.markdown("<h5 style='text-align: center; color: grey; font-style: italic'>*Get real-time metrics on similar brands/accounts at once! 🚀</h5>", unsafe_allow_html=True)
        st.write('')

        # creating columns
        col1, col2 = st.columns(2)

        with col1:
            # platform selection
            plat = st.radio("##### Select a platform",('🎦 Youtube', '📸 Instagram', '🎧 Spotify'),)
    
        # building out the instagram selection
        if plat == '📸 Instagram':
            with col2:
                # data type selection
                dat1 = st.radio("##### Select Comparison type",('📄 Basic', '📚 Advanced'))
            st.markdown('---')
            
            # building out the basic selection
            if dat1 == '📄 Basic':
                # text area input for multiple usernames
                usernames = st.text_area('###### Enter the accounts\' usernames below 👇', placeholder="Enter usernames separated by commas...", key="text_area", value='')

                # Split usernames by comma and strip any extra whitespace
                usernames_list = [username.strip() for username in usernames.split(",") if username.strip()]
                # Extract data for each username
                if st.button("⏬ Extract") or usernames_list:
                    for username in usernames_list:
                        try:
                            with st.spinner(f'Extracting data for {username}...'):
                                df = get_profile_metadata(username)
                            st.write(f"###### Here is {username}'s {dat1.split(' ')[0].lower()} metadata")
                            st.dataframe(df)

                        except Exception as e:
                            st.error(f"Oops! There was an error extracting data for {username}. Error: {e}")
            
            # building out the advanced selection
            if dat1 == '📚 Advanced':
                colA, colB, colC = st.columns([0.425, 0.15, 0.425])
                with colA:
                    # text input search bar
                    text = st.text_input('###### Enter the account\'s username below 👇',placeholder="search here...", key="text_input", value='')

                with colB:
                    st.write("") # just to create some space
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    button = st.button("🆚 Compare")
                
                with colC:
                    # text input search bar
                    text2 = st.text_input('###### Enter the account\'s username below 👇',placeholder="search here...", key="input_text", value='')

                st.markdown('---')

                if button or text and text2:
                    colX, colY = st.columns(2)
                    with colX:
                        try:
                            with st.spinner('Visualizing the data...'):
                                # Fetch the data
                                df = get_profile_metadata(text)

                            # Use the username in the output
                            st.write(f"Here is {text}'s profile metadata", unsafe_allow_html=True)

                            # Display Profile Picture prominently
                            #st.image(df['Profile Pic'].iloc[0], width=200, caption=f"{text}'s Profile Picture", use_column_width=False)

                            
                            st.markdown("""<style>.font {font-size:14px;}</style>""", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Username:</b> {df['User Name'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Full Name:</b> {df['Full Name'].iloc[0] if df['Full Name'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Biography:</b> {df['Biography'].iloc[0][:300] + '...' if len(df['Biography'].iloc[0]) > 300 else df['Biography'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Profile URL:</b> <a href='{df['Profile URL'].iloc[0]}' target='_blank'>{df['Profile URL'].iloc[0]}</a></div>", unsafe_allow_html=True)

                            colD, colE, colF = st.columns(3)
                            with colD:
                                formatted_followers = format_number(df['Followers'].iloc[0])
                                st.metric("Followers", formatted_followers)
                                
                            with colE:
                                formatted_following = format_number(df['Following'].iloc[0])
                                st.metric("Following", formatted_following)

                            with colF:
                                formatted_posts = format_number(df['Media Count'].iloc[0])
                                st.metric("Total Posts", formatted_posts,)  

                            metrics_style = "<style>.metrics {font-size:18px; font-weight:bold; color:white;} .submetrics {font-size:17px; color:grey;}</style>"

                            with colD:
                                total_likes = "{:,}".format(df['Total Likes'].iloc[0])
                                avg_likes = "{:,}".format(df['Average Likes'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Likes</div><div class='submetrics'>{total_likes}<br>Average: {avg_likes}</div>", unsafe_allow_html=True)
                                engagement_rate = "{:}".format(df['Engagement Rate'].iloc[0])   
                                st.markdown(metrics_style + f"<div class='metrics'>Engagement Rate</div><div class='submetrics'>{engagement_rate}</div>", unsafe_allow_html=True)

                            with colE:
                                total_comments = "{:,}".format(df['Total Comments'].iloc[0])
                                avg_comments = "{:,}".format(df['Average Comments'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Comments</div><div class='submetrics'>{total_comments}<br>Average: {avg_comments}</div>", unsafe_allow_html=True)

                            with colF:
                                total_views = "{:,}".format(df['Total Views'].iloc[0])
                                avg_views = "{:,}".format(df['Average Views'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Views</div><div class='submetrics'>{total_views}<br>Average: {avg_views}</div>", unsafe_allow_html=True)
                                estimated_reach = "{:,}".format(df['Estimated Reach'].iloc[0]) 
                                st.markdown(metrics_style + f"<div class='metrics'>Est. Reach</div><div class='submetrics'>{estimated_reach}</div>", unsafe_allow_html=True)                   

                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                        except:
                            st.error("Oops! Looks like this account doesn't exist, or there is a network error. Please cross-check your network connection and the username you entered!")

                    #Trying to show colX and colY simultaneously
                    with colY:
                        try:
                            with st.spinner('Visualizing the data...'):
                                # Fetch the data
                                df2 = get_profile_metadata(text2)

                            # Use the username in the output
                            st.write(f"Here is {text2}'s profile metadata", unsafe_allow_html=True)

                            # Display Profile Picture prominently
                            #st.image(df['Profile Pic'].iloc[0], width=200, caption=f"{text}'s Profile Picture", use_column_width=False)

                            
                            st.markdown("""<style>.font {font-size:14px;}</style>""", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Username:</b> {df2['User Name'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Full Name:</b> {df2['Full Name'].iloc[0] if df2['Full Name'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Biography:</b> {df2['Biography'].iloc[0][:300] + '...' if len(df2['Biography'].iloc[0]) > 300 else df2['Biography'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Profile URL:</b> <a href='{df2['Profile URL'].iloc[0]}' target='_blank'>{df2['Profile URL'].iloc[0]}</a></div>", unsafe_allow_html=True)

                            colD, colE, colF = st.columns(3)
                            with colD:
                                formatted_followers = format_number(df2['Followers'].iloc[0])
                                st.metric("Followers", formatted_followers)
                                
                            with colE:
                                formatted_following = format_number(df2['Following'].iloc[0])
                                st.metric("Following", formatted_following)

                            with colF:
                                formatted_posts = format_number(df2['Media Count'].iloc[0])
                                st.metric("Total Posts", formatted_posts,)  

                            metrics_style = "<style>.metrics {font-size:18px; font-weight:bold; color:white;} .submetrics {font-size:17px; color:grey;}</style>"

                            with colD:
                                total_likes = "{:,}".format(df2['Total Likes'].iloc[0])
                                avg_likes = "{:,}".format(df2['Average Likes'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Likes</div><div class='submetrics'>{total_likes}<br>Average: {avg_likes}</div>", unsafe_allow_html=True)
                                engagement_rate = "{:}".format(df['Engagement Rate'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Engagement Rate</div><div class='submetrics'>{engagement_rate}</div>", unsafe_allow_html=True)

                            with colE:
                                total_comments = "{:,}".format(df2['Total Comments'].iloc[0])
                                avg_comments = "{:,}".format(df2['Average Comments'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Comments</div><div class='submetrics'>{total_comments}<br>Average: {avg_comments}</div>", unsafe_allow_html=True)

                            with colF:
                                total_views = "{:,}".format(df2['Total Views'].iloc[0])
                                avg_views = "{:,}".format(df2['Average Views'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Views</div><div class='submetrics'>{total_views}<br>Average: {avg_views}</div>", unsafe_allow_html=True)
                                estimated_reach = "{:,}".format(df2['Estimated Reach'].iloc[0]) 
                                st.markdown(metrics_style + f"<div class='metrics'>Est. Reach</div><div class='submetrics'>{estimated_reach}</div>", unsafe_allow_html=True)

                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                        except:
                            st.error("Oops! Looks like this account doesn't exist, or there is a network error. Please cross-check your network connection and the username you entered!")
                    
                    colG, colH = st.columns(2)
                    #with colG:
                        #try:
                            # Pie chart for videos vs photos
                            #labels = ['Videos', 'Images']
                            #values = [df['Videos'].iloc[0], df['Images'].iloc[0]]
                            #fig = px.pie(names=labels, values=values, title="Videos vs Images Distribution")
                            #fig.update_traces(textinfo='value+percent', pull=[0.1, 0])
                            #fig.update_layout(width=300, height=400)  # Adjust the size as needed
                            #st.plotly_chart(fig)

                        #except Exception as e:
                            #st.error(f"An error occurred: {e}")
                        #except:
                            #st.error("Oops! Looks like this account doesn't exist, or there is a network error. Please cross-check your network connection and the username you entered!")

                    #with colH:
                        #try:
                            # Pie chart for videos vs photos
                            #labels = ['Videos', 'Images']
                            #values = [df2['Videos'].iloc[0], df2['Images'].iloc[0]]
                            #fig = px.pie(names=labels, values=values, title="Videos vs Images Distribution")
                            #fig.update_traces(textinfo='value+percent', pull=[0.1, 0])
                            #fig.update_layout(width=300, height=400)  # Adjust the size as needed
                            #st.plotly_chart(fig)

                        #except Exception as e:
                            #st.error(f"An error occurred: {e}")
                        #except:
                            #st.error("Oops! Looks like this account doesn't exist, or there is a network error. Please cross-check your network connection and the username you entered!")

                    colI, colJ = st.columns(2)
                    with colI:
                        try:
                            with st.spinner('Visualizing more data...'):
                                # Fetch the data
                                df_posts = get_post_metadata(text)
                            
                            # Normalize the 'Hashtags' column to ensure each row contains a list
                            df_posts['Hashtags'] = df_posts['Hashtags'].apply(lambda x: x if isinstance(x, list) else [x] if isinstance(x, str) else [])
                            
                            # Concatenate all hashtags into a single list
                            all_hashtags_list = sum(df_posts['Hashtags'].tolist(), [])
                            
                            # Join all hashtags in the list into a single string separated by spaces
                            all_hashtags_string = ' '.join(all_hashtags_list)

                            # Display the table
                            st.write("### Trending Posts")
                            df_filtered = df_posts[['Date', 'Post Type', 'Likes', 'Comments', 'Video Views', 'Post URL']]
                            st.dataframe(df_filtered, height=400)

                            # Generate the Word Cloud with adjusted parameters
                            wordcloud = WordCloud(
                                background_color='white',
                                max_words=200,
                                min_word_length=4,
                                width=2000,
                                height=1000
                            ).generate(all_hashtags_string)

                            # Display Word Cloud visual
                            st.write("### Trending Hashtags")
                            fig, ax = plt.subplots()
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)

                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                    with colJ:
                        try:
                            with st.spinner('Visualizing more data...'):
                                # Fetch the data
                                df_posts2 = get_post_metadata(text2)
                            
                            # Normalize the 'Hashtags' column to ensure each row contains a list
                            df_posts2['Hashtags'] = df_posts2['Hashtags'].apply(lambda x: x if isinstance(x, list) else [x] if isinstance(x, str) else [])
                            
                            # Concatenate all hashtags into a single list
                            all_hashtags_list = sum(df_posts2['Hashtags'].tolist(), [])
                            
                            # Join all hashtags in the list into a single string separated by spaces
                            all_hashtags_string = ' '.join(all_hashtags_list)
                            
                            # Display the table:
                            st.write("### Trending Posts")
                            df_filtered = df_posts2[['Date', 'Post Type', 'Likes', 'Comments', 'Video Views', 'Post URL']]
                            st.dataframe(df_filtered, height=400)

                            # Generate the Word Cloud with adjusted parameters
                            wordcloud = WordCloud(
                                background_color='white',
                                max_words=200,
                                min_word_length=4,
                                width=2000,
                                height=1000
                            ).generate(all_hashtags_string)

                            # Display Word Cloud visual
                            st.write("### Trending Hashtags")
                            fig, ax = plt.subplots()
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)

                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                    colK, colL = st.columns(2)
                    with colK:
                        try:
                            # Ensure 'Date' is a datetime object and extract the year
                            df_posts['Date'] = pd.to_datetime(df_posts['Date'])
                            df_posts['Year'] = df_posts['Date'].dt.year

                            # Filter the DataFrame to include only the past 5 years
                            current_year = pd.to_datetime('today').year
                            df_filtered = df_posts[df_posts['Year'] >= current_year - 5]

                            # Aggregate likes, comments, and views by year
                            aggregated_data = df_filtered.groupby('Year').agg({
                                'Likes': 'sum',
                                'Comments': 'sum',
                                'Video Views': 'sum'
                            }).reset_index()
                            
                            # Generate and display interactive bar charts
                            # Likes History
                            fig_likes = px.bar(aggregated_data, x='Year', y='Likes', title='Likes History Over the Past 5 Years', 
                                            text='Likes', color_discrete_sequence=["#636EFA"])
                            fig_likes.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Likes")
                            fig_likes.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                            
                            # Comments History
                            fig_comments = px.bar(aggregated_data, x='Year', y='Comments', title='Comments History Over the Past 5 Years', 
                                                text='Comments', color_discrete_sequence=["#EF553B"])
                            fig_comments.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Comments")
                            fig_comments.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                            
                            # Views History
                            fig_views = px.bar(aggregated_data, x='Year', y='Video Views', title='Views History Over the Past 5 Years', 
                                            text='Video Views', color_discrete_sequence=["#00CC96"])
                            fig_views.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Video Views")
                            fig_views.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                            
                            # Display the bar charts
                            st.plotly_chart(fig_likes, use_container_width=True)
                            st.plotly_chart(fig_comments, use_container_width=True)
                            st.plotly_chart(fig_views, use_container_width=True)
                        
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                    with colL:
                        try:
                            # Ensure 'Date' is a datetime object and extract the year
                            df_posts2['Date'] = pd.to_datetime(df_posts2['Date'])
                            df_posts2['Year'] = df_posts2['Date'].dt.year

                            # Filter the DataFrame to include only the past 5 years
                            current_year = pd.to_datetime('today').year
                            df_filtered = df_posts2[df_posts2['Year'] >= current_year - 5]

                            # Aggregate likes, comments, and views by year
                            aggregated_data = df_filtered.groupby('Year').agg({
                                'Likes': 'sum',
                                'Comments': 'sum',
                                'Video Views': 'sum'
                            }).reset_index()
                            
                            # Generate and display interactive bar charts
                            # Likes History
                            fig_likes = px.bar(aggregated_data, x='Year', y='Likes', title='Likes History Over the Past 5 Years', 
                                            text='Likes', color_discrete_sequence=["#636EFA"])
                            fig_likes.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Likes")
                            fig_likes.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                            
                            # Comments History
                            fig_comments = px.bar(aggregated_data, x='Year', y='Comments', title='Comments History Over the Past 5 Years', 
                                                text='Comments', color_discrete_sequence=["#EF553B"])
                            fig_comments.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Comments")
                            fig_comments.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                            
                            # Views History
                            fig_views = px.bar(aggregated_data, x='Year', y='Video Views', title='Views History Over the Past 5 Years', 
                                            text='Video Views', color_discrete_sequence=["#00CC96"])
                            fig_views.update_layout(xaxis={'type': 'category'}, yaxis_title="Total Video Views")
                            fig_views.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                            
                            # Display the bar charts
                            st.plotly_chart(fig_likes, use_container_width=True)
                            st.plotly_chart(fig_comments, use_container_width=True)
                            st.plotly_chart(fig_views, use_container_width=True)
                        
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                    colM, colN = st.columns(2)
                    with colM:
                        try:
                            with st.spinner('Visualizing more data...'):
                                # Fetch the data
                                df_mentions = get_mention_metadata(text)
                        
                            # Displaying a message to indicate data fetching is done
                            st.success('Data fetched successfully!')
                            
                            # Renaming and selecting specific columns for the display as per requirements
                            df_display = df_mentions[['Date', 'User Id', 'Post Type', 'Likes', 'Comments', 'Post URL']]
                            
                            # Setting the column names as needed
                            df_display.columns = ['Date', 'User ID', 'Post Type', 'Likes', 'Comments', 'URL']
                            
                            # Display the table as scrollable, adjusting height to show about 10 rows
                            st.write("### Trending Mentions")
                            st.dataframe(df_display, height=400)  # Adjust the height as needed to fit 10 rows visibly
                        
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                    
                    with colN:
                        try:
                            with st.spinner('Visualizing more data...'):
                                # Fetch the data
                                df_mentions2 = get_mention_metadata(text2)
                        
                            # Displaying a message to indicate data fetching is done
                            st.success('Data fetched successfully!')
                            
                            # Renaming and selecting specific columns for the display as per requirements
                            df_display = df_mentions2[['Date', 'User Id', 'Post Type', 'Likes', 'Comments', 'Post URL']]
                            
                            # Setting the column names as needed
                            df_display.columns = ['Date', 'User ID', 'Post Type', 'Likes', 'Comments', 'URL']
                            
                            # Display the table as scrollable, adjusting height to show about 10 rows
                            st.write("### Trending Mentions")
                            st.dataframe(df_display, height=400)  # Adjust the height as needed to fit 10 rows visibly
                        
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

        # building out the youtube selection
        if plat == '🎦 Youtube':
            with col2:
                # data type selection
                dat2 = st.radio("##### Select Comparison type",('📄 Basic', '📚 Advanced'))
            st.markdown('---')
            
            # building out the basic selection
            if dat2 == '📄 Basic':
                # text area input for multiple usernames
                usernames = st.text_area('###### Enter the Channels\' usernames below 👇', placeholder="Enter usernames separated by commas...", key="text_area", value='')

                # Split usernames by comma and strip any extra whitespace
                usernames_list = [username.strip() for username in usernames.split(",") if username.strip()]
                # Extract data for each username
                if st.button("⏬ Extract") or usernames_list:
                    for username in usernames_list:
                        try:
                            with st.spinner(f'Extracting data for {username}...'):
                                df, error_message, profile_pic_url = fetch_and_aggregate_channel_data(username)
                            st.write(f"###### Here is {username}'s {dat2.split(' ')[0].lower()} metadata")
                            st.image(profile_pic_url, caption='@' + username)
                            st.dataframe(df)

                        except Exception as e:
                            st.error(f"Oops! There was an error extracting data for {username}. Error: {e}")

            # building out the advanced selection
            if dat2 == '📚 Advanced':
                colA, colB, colC = st.columns([0.425, 0.15, 0.425])
                with colA:
                    # text input search bar
                    text = st.text_input('###### Enter the channel\'s username below 👇',placeholder="search here...", key="text_input", value='')

                with colB:
                    st.write("") # just to create some space
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    button = st.button("🆚 Compare")
                
                with colC:
                    # text input search bar
                    text2 = st.text_input('###### Enter the channel\'s username below 👇',placeholder="search here...", key="input_text", value='')

                st.markdown('---')

                if button or text and text2:
                    colX, colY = st.columns(2)
                    with colX:
                        try:
                            with st.spinner('Visualizing the data...'):
                                df, error_message, profile_pic_url = fetch_and_aggregate_channel_data(text)
                            if error_message:
                                st.write(error_message)

                            # Use the username in the output
                            st.write(f"Here is {text}'s profile metadata", unsafe_allow_html=True)

                            
                            st.image(profile_pic_url, caption='@'+text)
                            st.markdown("""<style>.font {font-size:14px;}</style>""", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Username:</b> {df['Title'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>About:</b> {df['Description'].iloc[0] if df['Description'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Country:</b> {df['Country'].iloc[0] if df['Country'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Channel URL:</b> <a href='{df['Channel URL'].iloc[0]}' target='_blank'>{df['Channel URL'].iloc[0]}</a></div>", unsafe_allow_html=True)
                            
                            colD, colE, colF = st.columns(3)
                            with colD:
                                formatted_followers = format_number(df['Subscriber Count'].iloc[0])
                                st.metric("Subscribers", formatted_followers)
                                
                            with colE:
                                formatted_posts = format_number(df['Total Videos'].iloc[0])
                                st.metric("Total Videos", formatted_posts)

                            with colF:
                                engagement_rate = "{:.2f}".format(df['Engagement Rate (%)'].iloc[0])
                                st.metric("Engagement Rate", engagement_rate + "%")

                            metrics_style = "<style>.metrics {font-size:18px; font-weight:bold; color:white;} .submetrics {font-size:17px; color:grey;}</style>"

                            with colD:
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                total_likes = "{:,}".format(df['Total Likes'].iloc[0])
                                avg_likes = "{:,}".format(df['Average Likes per Video'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Likes</div><div class='submetrics'>{total_likes}<br>Average: {avg_likes}</div>", unsafe_allow_html=True)

                            with colE:
                                estimated_reach = "{:,}".format(df['Estimated Reach'].iloc[0])  
                                st.markdown(metrics_style + f"<div class='metrics'>Est. Reach</div><div class='submetrics'>{estimated_reach}</div>", unsafe_allow_html=True)
                                total_comments = "{:,}".format(df['Total Comments'].iloc[0])
                                avg_comments = "{:,}".format(df['Average Comments per Video'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Comments</div><div class='submetrics'>{total_comments}<br>Average: {avg_comments}</div>", unsafe_allow_html=True)

                            with colF:
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                total_views = "{:,}".format(df['Total Views'].iloc[0])
                                avg_views = "{:,}".format(df['Average Views per Video'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Views</div><div class='submetrics'>{total_views}<br>Average: {avg_views}</div>", unsafe_allow_html=True)

                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                        except:
                            st.error("Oops! Looks like this account doesn't exist, or there is a network error. Please cross-check your network connection and the username you entered!")

                    with colY:
                        try:
                            with st.spinner('Visualizing the data...'):
                                df2, error_message, profile_pic_url = fetch_and_aggregate_channel_data(text2)
                            if error_message:
                                st.write(error_message)

                            # Use the username in the output
                            st.write(f"Here is {text2}'s profile metadata", unsafe_allow_html=True)

                            
                            st.image(profile_pic_url, caption='@'+text2)
                            st.markdown("""<style>.font {font-size:14px;}</style>""", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Username:</b> {df2['Title'].iloc[0]}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>About:</b> {df2['Description'].iloc[0] if df2['Description'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Country:</b> {df2['Country'].iloc[0] if df2['Country'].iloc[0] else 'N/A'}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='font'><b>Channel URL:</b> <a href='{df2['Channel URL'].iloc[0]}' target='_blank'>{df2['Channel URL'].iloc[0]}</a></div>", unsafe_allow_html=True)
                            
                            colD, colE, colF = st.columns(3)
                            with colD:
                                formatted_followers = format_number(df2['Subscriber Count'].iloc[0])
                                st.metric("Subscribers", formatted_followers)
                                
                            with colE:
                                formatted_posts = format_number(df2['Total Videos'].iloc[0])
                                st.metric("Total Videos", formatted_posts)

                            with colF:
                                engagement_rate = "{:.2f}".format(df2['Engagement Rate (%)'].iloc[0])
                                st.metric("Engagement Rate", engagement_rate + "%")  

                            metrics_style = "<style>.metrics {font-size:18px; font-weight:bold; color:white;} .submetrics {font-size:17px; color:grey;}</style>"

                            with colD:
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                total_likes = "{:,}".format(df2['Total Likes'].iloc[0])
                                avg_likes = "{:,}".format(df2['Average Likes per Video'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Likes</div><div class='submetrics'>{total_likes}<br>Average: {avg_likes}</div>", unsafe_allow_html=True)

                            with colE:
                                estimated_reach = "{:,}".format(df2['Estimated Reach'].iloc[0])  
                                st.markdown(metrics_style + f"<div class='metrics'>Est. Reach</div><div class='submetrics'>{estimated_reach}</div>", unsafe_allow_html=True)
                                total_comments = "{:,}".format(df2['Total Comments'].iloc[0])
                                avg_comments = "{:,}".format(df2['Average Comments per Video'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Comments</div><div class='submetrics'>{total_comments}<br>Average: {avg_comments}</div>", unsafe_allow_html=True)

                            with colF:
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                st.markdown("")
                                total_views = "{:,}".format(df2['Total Views'].iloc[0])
                                avg_views = "{:,}".format(df2['Average Views per Video'].iloc[0])
                                st.markdown(metrics_style + f"<div class='metrics'>Number of Views</div><div class='submetrics'>{total_views}<br>Average: {avg_views}</div>", unsafe_allow_html=True)

                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                        except:
                            st.error("Oops! Looks like this account doesn't exist, or there is a network error. Please cross-check your network connection and the username you entered!")

                    colQ, colZ = st.columns(2)
                    with colQ:
                        try:
                            with st.spinner('Visualizing more data...'):
                                df = fetch_videos_and_details(text) 
                                # Ensure 'Date' is a datetime object and extract the year
                                df['Date Posted'] = pd.to_datetime(df['Date Posted'])
                                df['Year'] = df['Date Posted'].dt.year

                                # Filter the DataFrame to include only the past 5 years
                                current_year = pd.to_datetime('today').year
                                df_filtered = df[df['Year'] >= current_year - 5]

                                # Aggregate likes, comments, and views by year
                                aggregated_data = df_filtered.groupby('Year').agg({
                                    'Likes': 'sum',
                                    'Comments': 'sum',
                                    'Views': 'sum'
                                }).reset_index()
                            
                                # Plotting the bar charts
                                fig_likes = px.bar(aggregated_data, x='Year', y='Likes', title='Likes History Over the Past 5 Years',
                                                    color_discrete_sequence=["#636EFA"])
                                fig_comments = px.bar(aggregated_data, x='Year', y='Comments', title='Comments History Over the Past 5 Years',
                                                        color_discrete_sequence=["#EF553B"])
                                fig_views = px.bar(aggregated_data, x='Year', y='Views', title='Views History Over the Past 5 Years',
                                                    color_discrete_sequence=["#00CC96"])

                                st.plotly_chart(fig_likes, use_container_width=True)
                                st.plotly_chart(fig_comments, use_container_width=True)
                                st.plotly_chart(fig_views, use_container_width=True)
                        
                                #Setting up a Table for posts
                                
                                # Renaming and selecting specific columns for the display as per requirements
                                df_display = df[['Title', 'Date Posted', 'Description', 'Views', 'Likes', 'Comments', 'URL']]
                                
                                # Setting the column names as needed
                                df_display.columns = ['Title', 'Date', 'Description', 'Views', 'Likes', 'Comments', 'URL']
                                
                                # Display the table as scrollable, adjusting height to show about 10 rows
                                st.write("### Channel Posts")
                                st.dataframe(df_display, height=400)  # Adjust the height as needed to fit 10 rows visibly
                            
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                    with colZ:
                        try:
                            with st.spinner('Visualizing more data...'):
                                df2 = fetch_videos_and_details(text2) 
                                # Ensure 'Date' is a datetime object and extract the year
                                df2['Date Posted'] = pd.to_datetime(df2['Date Posted'])
                                df2['Year'] = df2['Date Posted'].dt.year

                                # Filter the DataFrame to include only the past 5 years
                                current_year = pd.to_datetime('today').year
                                df_filtered = df2[df2['Year'] >= current_year - 5]

                                # Aggregate likes, comments, and views by year
                                aggregated_data = df_filtered.groupby('Year').agg({
                                    'Likes': 'sum',
                                    'Comments': 'sum',
                                    'Views': 'sum'
                                }).reset_index()
                            
                                # Plotting the bar charts
                                fig_likes = px.bar(aggregated_data, x='Year', y='Likes', title='Likes History Over the Past 5 Years',
                                                    color_discrete_sequence=["#636EFA"])
                                fig_comments = px.bar(aggregated_data, x='Year', y='Comments', title='Comments History Over the Past 5 Years',
                                                        color_discrete_sequence=["#EF553B"])
                                fig_views = px.bar(aggregated_data, x='Year', y='Views', title='Views History Over the Past 5 Years',
                                                    color_discrete_sequence=["#00CC96"])

                                st.plotly_chart(fig_likes, use_container_width=True)
                                st.plotly_chart(fig_comments, use_container_width=True)
                                st.plotly_chart(fig_views, use_container_width=True)
                        
                                #Setting up a Table for posts
                                
                                # Renaming and selecting specific columns for the display as per requirements
                                df_display = df2[['Title', 'Date Posted', 'Description', 'Views', 'Likes', 'Comments', 'URL']]
                                
                                # Setting the column names as needed
                                df_display.columns = ['Title', 'Date', 'Description', 'Views', 'Likes', 'Comments', 'URL']
                                
                                # Display the table as scrollable, adjusting height to show about 10 rows
                                st.write("### Channel Posts")
                                st.dataframe(df_display, height=400)  # Adjust the height as needed to fit 10 rows visibly
                            
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

        # building out the spotify selection
        if plat == '🎧 Spotify':
            with col2:
                # data type selection
                dat2 = st.radio("##### Select the kind of data you need", ('👨‍🎤 Artist `metadata`', '🎙️ Podcast `metadata`'))
            st.markdown('---')
            
            # building out the Artist selection
            if dat2 == '👨‍🎤 Artist `metadata`':
                # text area input for multiple usernames
                usernames = st.text_area('###### Enter the accounts\' usernames below 👇', placeholder="Enter usernames separated by commas...", key="text_area", value='')

                # Split usernames by comma and strip any extra whitespace
                usernames_list = [username.strip() for username in usernames.split(",") if username.strip()]

                # Extract data for each username
                if st.button("⏬ Extract", key="spotify_extract_button") or usernames_list:
                    for username in usernames_list:
                        try:
                            with st.spinner(f'Extracting data for {username}...'):
                                result = get_artist_data(username)
                                if result:
                                    artist_df, top_tracks_df, image_url = result
                                    if not artist_df.empty:
                                        st.write(f"###### Here is {username}'s {dat2.split(' ')[0].lower()} metadata")
                                        if image_url:
                                            st.image(image_url, caption=f'@{username}', width=100)
                                        st.dataframe(artist_df)
                                    else:
                                        st.write(f"No top tracks data available for {username}")
                        except Exception as e:
                            st.error(f"Oops! There was an error extracting data for {username}. Error: {e}")

            # building out the podcast selection
            if dat2 == '🎙️ Podcast `metadata`':
                # text area input for multiple usernames
                usernames = st.text_area('###### Enter the accounts\' usernames below 👇', placeholder="Enter usernames separated by commas...", key="text_area", value='')

                # Split usernames by comma and strip any extra whitespace
                usernames_list = [username.strip() for username in usernames.split(",") if username.strip()]

                # Extract data for each username
                if st.button("⏬ Extract", key="spotify_extract_button") or usernames_list:
                    for username in usernames_list:
                        try:
                            with st.spinner(f'Extracting data for {username}...'):
                                result = get_podcast_data(username)
                                if result:
                                    podcast_df, episodes_df = result
                                    name = podcast_df["Podcast Name"][0]
                                    if not podcast_df.empty:
                                        st.write(f"###### Here is {name}'s {dat2.split(' ')[0].lower()} metadata")
                                        if podcast_df['Image URL'][0] != 'N/A':
                                            st.image(podcast_df['Image URL'][0], caption=f'@{name}', width=100)
                                        st.dataframe(podcast_df)
                                    else:
                                        st.write(f"No top tracks data available for {name}")
                        except Exception as e:
                            st.error(f"Oops! There was an error extracting data for {username}. Error: {e}")
############################################################# SOLUTION OVERVIEW PAGE ###################################################################
    if page_selection == "Solution Overview":
        # Header contents
        st.image('resources/imgs/tima_logo.png',use_column_width=True,)
        st.markdown("<h3 style='text-align: center; color: #82E0AA;'>💡 Solution Overview</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: grey; font-style: italic'>TIMA\'s portal for social media data sourcing 📊</h5>", unsafe_allow_html=True)
        st.markdown('---')
        st.write("""
        **TIMA** Social Data Center is a comprehensive tool designed for social media data analysis.
                 This portal enables users to visualize various metrics for social media accounts,
                 providing insights on followers, likes, comments, engagement rates, estimated reach and more.
                 Currently, it supports:

        - 🎦 YouTube
        - 📸 Instagram
        - 🎧 Spotify

        ### Features
        - **Ready-made Visuals:**   Get pre-defined visualizations for social media accounts.
        - **Custom-made Visuals:**  Customize the visuals as per your requirements.
        - **Data Download:**    Download the data for offline analysis.
        - **Export Visuals:**   Export generated visuals for presentations and data reporting.
        """)

    # You may want to add more sections here for other aspects such as company profile.


if __name__ == '__main__':
    main()
