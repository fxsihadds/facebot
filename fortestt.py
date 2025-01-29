import requests
import os

# URL to the file
url = "https://snap-insta.app/wp-content/plugins/visolix-video-downloader/dl.php?id=e0a13c3cfa&countdown=0"

# Specify the folder where you want to save the file
folder_path = "commands/cache"

# Make sure the folder exists, if not, create it
os.makedirs(folder_path, exist_ok=True)

# Full path including filename where the file will be saved
file_path = os.path.join(folder_path, "video.mp4")

# Send the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Write the content to the file
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"Download successful! File saved to {file_path}")
else:
    print(f"Failed to download. Status code: {response.status_code}")
