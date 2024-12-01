import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the user token from environment variables
USER_TOKEN = os.getenv('USER_TOKEN')  # Fetch token from .env file
CHANNEL_ID = '769451104680804402'  # Replace with your actual channel ID

# Ensure the token is loaded
if not USER_TOKEN:
    raise ValueError("USER_TOKEN not found in environment variables.")

# Set the download path to a folder named 'Downloads' within the project directory
DOWNLOAD_PATH = os.path.join(os.getcwd(), "photo")

# Create the download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)
    print(f"Download directory created at {DOWNLOAD_PATH}")

def download_image(url, filename):
    """Downloads the image from the URL to the specified folder."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(DOWNLOAD_PATH, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f'Downloaded {filename} to {file_path}')
    else:
        print(f'Failed to download {filename}')

def fetch_channel_messages():
    """Fetches messages from the specified Discord channel."""
    headers = {
        "Authorization": USER_TOKEN  # Use the correct user token here without any prefix
    }
    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"  # Make sure to use the correct CHANNEL_ID
    params = {
        "limit": 100  # Number of messages to fetch per request (100 is the max)
    }

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Failed to fetch messages")
            print(f"Response Code: {response.status_code}")
            print(f"Error: {response.text}")
            break

        messages = json.loads(response.text)

        if not messages:
            print("No more messages to process")
            break

        for message in messages:
            for attachment in message.get("attachments", []):
                if any(attachment["filename"].endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                    download_image(attachment["url"], attachment["filename"])

        # Get the ID of the last message to continue from where we left off
        params["before"] = messages[-1]["id"]

# Start downloading images
fetch_channel_messages()
