"""

    Helper functions for extracting the
    account's profile mentions.

    Author: Kenechukwu Ozojie.

"""

# Import required Libraries
import instaloader
import pandas as pd

# Create a function that extracts post mentions for a profile
def get_mention_metadata(username):
    # Create an Instaloader instance
    L = instaloader.Instaloader()

    # Set up a profile for the account you want to get post mentions for
    profile = instaloader.Profile.from_username(L.context, username)

    # Create a list to store the data
    data = []
    
    # Create counter to limit the number of posts
    post_count = 0
    limit = 100

    # Iterate through the posts and extract relevant information
    for post in profile.get_tagged_posts():
        data.append([
            post.owner_id,
            post.date,
            f'https://www.instagram.com/p/{post.shortcode}/',
            post.likes,
            post.comments,
            post.caption,
            ', '.join(post.caption_mentions),
            ', '.join(post.caption_hashtags),
            'Video' if post.is_video else 'Image',
            post.video_view_count if post.is_video else None,
            post.url.rstrip('?utm_source=ig_web_copy_link')  # Shorten the URL if needed
        ])

        # Increment the counter
        post_count += 1

        # Break the loop if the limit is reached
        if post_count >= limit:
            break

        # Write the data to a pandas dataframe
        column_list = ['User Id', 'Date', 'Post URL', 'Likes', 
                     'Comments', 'Caption', 'Mentions', 'Hashtags',
                     'Post Type', 'Video Views', 'Shortened URL']
        df = pd.DataFrame(data=data, columns= column_list)

    return df