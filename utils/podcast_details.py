# Import libraries
import streamlit as st
import requests
import base64
import pandas as pd

# Spotify API credentials
client_id = 'b6961159550e4f3b823e5890002e27a9'
client_secret = '98cee7f07b514488a375ba4985f1448b'

@st.cache_data(ttl=10800, show_spinner=False)
def get_access_token():
    token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    headers = {
        "Authorization": f"Basic {client_creds_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(token_url, headers=headers, data=data)
    token_response = response.json()
    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        print("Failed to get access token:", token_response.get('error', 'Unknown error'))
        return None

@st.cache_data(ttl=10800, show_spinner=False)
def get_podcast_details(podcast_id, access_token):
    podcast_endpoint = f"https://api.spotify.com/v1/shows/{podcast_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(podcast_endpoint, headers=headers)
    
    response_json = response.json()
    if 'error' in response_json:
        print("Error fetching podcast details:", response_json['error']['message'])
        return None
    
    podcast_data = {
        'Podcast Name': response_json.get('name', 'N/A'),
        'Publisher': response_json.get('publisher', 'N/A'),
        'Total Episodes': response_json.get('total_episodes', 'N/A'),
        'Description': response_json.get('description', 'N/A'),
        'Languages': ', '.join(response_json.get('languages', [])),
        'Media Type': response_json.get('media_type', 'N/A'),
        'Link': response_json.get('external_urls', {}).get('spotify', 'N/A'),
        'Copyrights': ', '.join(copyright['text'] for copyright in response_json.get('copyrights', [])),
        'Explicit': response_json.get('explicit', 'N/A'),
        'Image URL': response_json.get('images', [{}])[0].get('url', 'N/A')  # Get the image URL
    }
    
    return podcast_data

@st.cache_data(ttl=10800, show_spinner=False)
def get_recent_episodes(podcast_id, access_token, limit=100):
    episodes_endpoint = f"https://api.spotify.com/v1/shows/{podcast_id}/episodes"
    headers = {"Authorization": f"Bearer {access_token}"}
    episodes_data = []
    params = {"limit": 50}
    
    while len(episodes_data) < limit:
        response = requests.get(episodes_endpoint, headers=headers, params=params)
        response_json = response.json()
        
        if 'error' in response_json:
            print("Error fetching episodes:", response_json['error']['message'])
            break
        
        episodes_data.extend(response_json.get('items', []))
        
        if len(response_json.get('items', [])) < 50 or not response_json.get('next'):
            break
        
        params["offset"] = len(episodes_data)
    
    episode_details = []
    for episode in episodes_data[:limit]:
        episode_info = {
            'Episode Name': episode.get('name', 'N/A'),
            'Description': episode.get('description', 'N/A'),
            'Release Date': episode.get('release_date', 'N/A'),
            'Duration (ms)': episode.get('duration_ms', 'N/A'),
            'Explicit': episode.get('explicit', 'N/A'),
            'Language': ', '.join(episode.get('languages', [])),
            'Link': episode.get('external_urls', {}).get('spotify', 'N/A')
        }
        episode_details.append(episode_info)
    
    return pd.DataFrame(episode_details)

@st.cache_data(ttl=10800, show_spinner=False)
def get_podcast_data(podcast_id):
    access_token = get_access_token()
    if not access_token:
        return None

    podcast_details = get_podcast_details(podcast_id, access_token)
    episodes_df = get_recent_episodes(podcast_id, access_token)
    
    if podcast_details and not episodes_df.empty:
        podcast_df = pd.DataFrame([podcast_details])
        return podcast_df, episodes_df
    else:
        return None
