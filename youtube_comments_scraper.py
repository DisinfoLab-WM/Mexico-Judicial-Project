import json
import pandas as pd
from dotenv import dotenv_values
from googleapiclient.discovery import build

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

DEVELOPER_KEY = config['DEVELOPER_KEY']  # put your own key here
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

combined_df = pd.DataFrame([], columns=['author', 'updated_at', 'like_count', 'text', 'public'])

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# video_id_list = ['fijHG938buA', 'vOgKeEvcfFU', '3dhJg5lsfcw', '3dhJg5lsfcw', 'REOopTSnfyY', 'PFwo3gMBboo', 'c28JUY7AXcw', 'aAPtnfIiAYw']
video_id_list = ['9vp_LE1Xm94', '2GgEAv5Pow4', 'jFqxizE2aQ0', 'hRJ6_L6BfYo', 'm93aYPICNg8', 'oB5w4KHMJf4', 'pbfIhof8LJw', 'Xcylgw4japA', 'GMgT7TcEnmw', '4X7VyXMSiQo', 'SnsgP3HbrWg', 'zNlyxFsVogI', 'Oj89FwD1oYA']


json_filename = './mexico_judicial_search6.json'  # change to save to different file
csv_filename = './mexico_judicial_search6.csv'

# Fetch comments for each video
for video_id in video_id_list:
    print(f"Fetching comments for video: {video_id}")
    
    # Initialize the request for the first page of comments
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        order="relevance"
    )

    comments = []

    # Fetch comments while there is a nextPageToken
    while request:
        try:
            response = request.execute()
        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            break

        # Extract comments from the response
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            public = item['snippet']['isPublic']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textOriginal'],

                public
            ])

        # Check for nextPageToken
        next_page_token = response.get('nextPageToken')
        if next_page_token:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                order="relevance",
                pageToken=next_page_token  # Use the nextPageToken to get the next page
            )
        else:
            request = None  # No more pages, stop the loop

    # Create a DataFrame for the comments and append to combined_df
    df1 = pd.DataFrame(comments, columns=['author', 'updated_at', 'like_count', 'text', 'public'])
    combined_df = pd.concat([combined_df, df1], ignore_index=True)

# Save the combined comments to a CSV
combined_df.to_csv(csv_filename, index=False)

print("Comments saved to CSV.")
