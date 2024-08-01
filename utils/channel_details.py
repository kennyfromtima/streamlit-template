"""

    Helper functions for extracting the
    account's youtube channel details.

    Author: Todimu Pitan.

"""

# Import required Libraries
import streamlit as st
from googleapiclient.discovery import build
import pandas as pd

# API key (replace with yours)
api_key = 'AIzaSyBGf2wn9gHL6TyOTc7sUyABsWHLkDpqPHM'
youtube = build('youtube', 'v3', developerKey=api_key)

@st.cache_data(ttl=10800, show_spinner=False)
def search_channel_by_name(channel_name):
    # Use the YouTube API search endpoint to locate the channel by a given name or identifier
    search_response = youtube.search().list(
        q=channel_name,
        part='snippet',
        type='channel',
        maxResults=1
    ).execute()
    
    if search_response['items']:
        channel_id = search_response['items'][0]['id']['channelId']
        return channel_id
    else:
        return None

@st.cache_data(ttl=10800, show_spinner=False)
def fetch_and_aggregate_channel_data(username):
    # Search channel ID by name
    channel_id = search_channel_by_name(username)
    if not channel_id:
        return None, "Channel not found for the given name.", None
    
    try:
        # Fetch channel details including uploads playlist ID
        channel_response = youtube.channels().list(part='contentDetails,snippet,statistics', id=channel_id).execute()
        if not channel_response.get('items'):
            return None, "Channel details not available.", None

        channel_data = channel_response['items'][0]
        playlist_id = channel_data['contentDetails']['relatedPlaylists']['uploads']
        profile_picture_url = channel_data['snippet']['thumbnails']['default']['url']  # Profile picture URL

        # Initialize aggregation variables
        total_likes, total_comments, total_views, video_count = 0, 0, 0, 0
        video_ids = []
        next_page_token = None

        # Fetch all video IDs from the playlist
        while True:
            playlist_response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            video_ids += [video['contentDetails']['videoId'] for video in playlist_response.get('items', [])]
            next_page_token = playlist_response.get('nextPageToken')
            
            if not next_page_token:
                break

        # Fetch video statistics in batches
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            video_response = youtube.videos().list(
                part='statistics',
                id=','.join(batch_ids)
            ).execute()

            for item in video_response.get('items', []):
                stats = item.get('statistics', {})
                total_likes += int(stats.get('likeCount', 0))
                total_comments += int(stats.get('commentCount', 0))
                total_views += int(stats.get('viewCount', 0))

        video_count = len(video_ids)

        # Calculating averages and engagement rate
        average_likes = total_likes / video_count if video_count else 0
        average_comments = total_comments / video_count if video_count else 0
        average_views = total_views / video_count if video_count else 0
        subscriber_count = int(channel_data['statistics']['subscriberCount'])
        engagement_rate = ((total_likes + total_comments) / subscriber_count) if subscriber_count else 0
        estimated_reach = (engagement_rate * subscriber_count) * 1.5
        
        # Compiling data into a DataFrame
        aggregated_data = pd.DataFrame([{
            'Title': channel_data['snippet']['title'],
            'Description': channel_data['snippet']['description'],
            'Country': channel_data['snippet'].get('country', 'Not provided'),
            'Subscriber Count': subscriber_count,
            'Total Views': total_views,
            'Total Videos': video_count,
            'Total Likes': total_likes,
            'Total Comments': total_comments,
            'Average Likes per Video': round(average_likes,2),
            'Average Comments per Video': round(average_comments,2),
            'Average Views per Video': round(average_views,2),
            'Engagement Rate (%)': round(engagement_rate,2),
            'Estimated Reach' : round(estimated_reach,2),
            'Channel URL': f"https://www.youtube.com/channel/{channel_id}"
        }])

        return aggregated_data, None , profile_picture_url
    
    except Exception as e:
        return None, str(e), None