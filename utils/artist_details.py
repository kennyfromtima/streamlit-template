import requests
import base64
import pandas as pd

# Spotify API credentials
client_id = 'b6961159550e4f3b823e5890002e27a9'
client_secret = '98cee7f07b514488a375ba4985f1448b'

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

def fetch_artist_details(artist_name, access_token):
    """Fetch artist details by name from Spotify."""
    search_endpoint = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}
    search_response = requests.get(search_endpoint, headers=headers, params=params).json()
    
    if not search_response.get('artists', {}).get('items'):
        print("No artist found with the name:", artist_name)
        return pd.DataFrame(), None  # Return an empty DataFrame and None for artist_id
    
    artist = search_response['artists']['items'][0]
    artist_id = artist['id']
    
    artist_details_endpoint = f"https://api.spotify.com/v1/artists/{artist_id}"
    artist_response = requests.get(artist_details_endpoint, headers=headers).json()

    artist_data = {
        'Artist Name': artist.get('name', 'N/A'),
        'Followers': artist_response.get('followers', {}).get('total', 0),
        'Popularity': artist_response.get('popularity', 0),
        'Genres': ', '.join(artist_response.get('genres', [])),
        'Profile Link': artist.get('external_urls', {}).get('spotify', 'N/A')
    }
    
    return pd.DataFrame([artist_data]), artist_id

def fetch_artist_top_tracks(artist_id, access_token):
    """Fetch top tracks of an artist from Spotify and include popularity data."""
    if artist_id is None:
        return pd.DataFrame()  # Return an empty DataFrame if artist_id is None
    
    top_tracks_endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"country": "US"}
    response = requests.get(top_tracks_endpoint, headers=headers, params=params).json()
    
    if 'tracks' not in response:
        print("Failed to fetch top tracks.")
        return pd.DataFrame()

    top_tracks = [{
        'Track Name': track['name'],
        'Popularity': track['popularity'],
        'Album Name': track['album']['name'],
        'Release Date': track['album']['release_date']
    } for track in response['tracks']]

    return pd.DataFrame(top_tracks)

def get_artist_data(artist_name):
    """Main function to retrieve and display artist data and top tracks."""
    access_token = get_access_token()
    if not access_token:
        return

    artist_df, artist_id = fetch_artist_details(artist_name, access_token)
    if artist_df.empty:
        print("No data available for the artist.")
        return

    top_tracks_df = fetch_artist_top_tracks(artist_id, access_token)
    if top_tracks_df.empty:
        print("No top tracks data available.")

    return artist_df, top_tracks_df
