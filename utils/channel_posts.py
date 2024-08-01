"""

    Helper functions for extracting the
    account's youtube channel posts.

    Author: Todimu Pitan.

"""
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
def fetch_videos_and_details(username, max_videos=1000):
    # Search channel ID by name
    channel_id = search_channel_by_name(username)
    if not channel_id:
        return None, "Channel not found for the given name.", None

    # Fetch uploads playlist ID
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    #profile_picture_url = channel_response['items'][0]['snippet']['thumbnails']['default']['url']
    
    # Initialize list for video IDs and counter
    video_ids = []
    video_count = 0
    next_page_token = None
    
    # Fetch up to max_videos video IDs from the playlist
    while video_count < max_videos:
        playlist_response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        batch_ids = [video['contentDetails']['videoId'] for video in playlist_response['items']]
        video_ids.extend(batch_ids)
        video_count += len(batch_ids)
        next_page_token = playlist_response.get('nextPageToken')
        
        if next_page_token is None or video_count >= max_videos:
            break
    
    video_ids = video_ids[:max_videos]  # Ensure we only process up to max_videos
    videos_data = []
    
    # Fetch video details in batches of 50
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(batch_ids)
        ).execute()
        
        for item in video_response['items']:
            stats = item['statistics']
            snippet = item['snippet']
            video_id = item['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            view_count = int(stats.get('viewCount', 0))
            like_count = int(stats.get('likeCount', 0))
            comment_count = int(stats.get('commentCount', 0))
            description = snippet.get('description', '')
            hashtags = [word for word in description.split() if word.startswith('#')]
            engagement_rate = ((like_count + comment_count) / view_count) * 100 if view_count > 0 else 0
            
            videos_data.append({
                'Title': snippet['title'],
                'Date Posted': snippet['publishedAt'],
                'Views': view_count,
                'Likes': like_count,
                'Comments': comment_count,
                'Description': description,
                'Hashtags': ', '.join(hashtags),
                'Engagement Rate': round(engagement_rate,2),
                'URL': video_url
            })
            
    # Convert list of dicts to DataFrame
    videos_df = pd.DataFrame(videos_data)

    return videos_df
