import requests
from bs4 import BeautifulSoup
import re
import json
from concurrent.futures import ThreadPoolExecutor
import sys

BASE_URL = 'https://www3.animeflv.net'

def fetch_url(url):
    """Makes an HTTP request to the URL and returns the HTML content if successful."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error if the response is not 200
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None

def get_anime_info(response_text):
    """Gets the anime name and the number of episodes from the HTML content."""
    anime_name = None
    number_episodes = 0
    
    # Search for the 'anime_info' array using a regular expression
    match = re.search(r'var anime_info = (\[.*?\]);', response_text, re.DOTALL)
    if match:
        anime_info_data = json.loads(match.group(1))  # Use json.loads instead of eval
        anime_name = anime_info_data[2]
    
    # Search for the 'episodes' array
    match = re.search(r'var episodes = (\[\[.*?\]\]);', response_text, re.DOTALL)
    if match:
        episodes_data = json.loads(match.group(1))
        number_episodes = len(episodes_data)
    
    return anime_name, number_episodes

def get_servers_from_video_page(url):
    """Gets the video servers for an episode page."""
    response_text = fetch_url(url)
    if response_text:
        # Create the BeautifulSoup object
        soup = BeautifulSoup(response_text, 'html.parser')
        
        # Find all scripts
        scripts = soup.find_all('script')
        
        # Search for the "videos" variable
        for script in scripts:
            if script.string:
                match = re.search(r'var videos\s*=\s*(\{.*?\});', script.string, re.DOTALL)
                if match:
                    videos_json = match.group(1)  # Capture the JSON as a string
                    try:
                        videos_data = json.loads(videos_json)
                        servers_data = {video.get("server"): video.get("code") for video in videos_data.get("SUB", [])}
                        return servers_data
                    except json.JSONDecodeError:
                        print("Error decoding the videos JSON.")
                        return None
    return None

def get_episodes_from_video_page(base_url, url):
    """Gets the list of episode URLs from the anime page."""
    response_text = fetch_url(url)
    if response_text:
        anime_name, number_episodes = get_anime_info(response_text)
        if anime_name and number_episodes:
            # Create the array of URLs
            return [f"{base_url}/ver/{anime_name}-{i}" for i in range(1, number_episodes + 1)]
    return []

def get_all_servers_data(base_url, url):
    """Gets all server data for all episodes."""
    episode_list = get_episodes_from_video_page(base_url, url)
    episodes_data = {}

    with ThreadPoolExecutor() as executor:
        # Use ThreadPoolExecutor to fetch server data concurrently
        results = executor.map(get_servers_from_video_page, episode_list)
        
        # Store the results in the dictionary
        for index, servers_data in enumerate(results):
            if servers_data:
                episodes_data[index + 1] = servers_data
    
    return episodes_data

def main():
    # Read the first argument (the script itself is the first argument)
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("No URL provided.")
        return -1

    episodes_data = get_all_servers_data(BASE_URL, url)

    # Convert the dictionary to JSON format and display it
    episodes_json = json.dumps(episodes_data, indent=4)
    print(episodes_json)

if __name__ == "__main__":
    main()
