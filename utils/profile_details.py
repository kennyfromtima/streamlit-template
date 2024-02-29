"""

    Helper functions for extracting the
    account's profile details.

    Author: Kenechukwu Ozojie.

"""

# Import required Libraries
import instaloader
import pandas as pd

# Create a function that extracts data from a profile
def get_profile_metadata(username):
    # Create an Instaloader instance
    L = instaloader.Instaloader()

    # Set up a profile for the account you want to get data from
    profile = instaloader.Profile.from_username(L.context, username)

    # Initialize variables for total likes, comments, and video views
    total_likes = 0
    total_comments = 0
    total_video_views = 0
    total_posts = profile.mediacount
    videos = 0
    images = 0

    # Iterate through the user's posts to calculate totals
    for post in profile.get_posts():
        total_likes += post.likes
        total_comments += post.comments
        if post.is_video:
            total_video_views += post.video_view_count
            videos += 1
        else:
            images += 1

    # Calculating averages
    avg_likes = round(total_likes / total_posts,2)
    avg_comments = round(total_comments / total_posts,2)
    avg_views = round(total_video_views / total_posts,2)
    engagement_rate = round(((total_likes + total_comments) / profile.followers),2)
    
    # calculating rates
    likes_rate = round(total_likes/profile.followers,2)
    comments_rate = round(total_comments/profile.followers,2)
    views_rate = round(total_video_views/profile.followers,2)
    # Create a list to store the data
    data = []

    # Iterate through the profile and extract relevant information
    data.append([
        f"@{profile.username}",
        profile.full_name,
        profile.biography,
        profile.followers,
        profile.followees,
        total_likes,
        avg_likes,
        f"{likes_rate}%",
        total_comments,
        avg_comments,
        f"{comments_rate}%",
        total_video_views,
        avg_views,
        f"{views_rate}%",
        f"{engagement_rate}%",
        videos,
        images,
        profile.is_private,
        profile.is_verified,
        total_posts,
        profile.profile_pic_url,
        f"https://instagram.com/{username}"])
    
    # Write the data to a pandas dataframe
    column_list= ['User Name', 'Full Name', 'Biography', 'Followers',
                     'Following', 'Total Likes', 'Average Likes', 'Likes Rate', 'Total Comments',
                     'Average Comments', 'Comments Rate', 'Total Views', 'Average Views', 'Views Rate',
                     'Engagement Rate', 'Videos', 'Images', 'Private', 'Verified',
                     'Media Count', 'Profile Pic','Profile URL']
    df = pd.DataFrame(data=data, columns= column_list)

    return df