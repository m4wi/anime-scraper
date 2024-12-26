# Anime FLV Scraper

This project is a **scraper** for retrieving episode information and video server details from the **AnimeFLV** website. It uses multithreading to fetch data concurrently, improving performance.

## Description

This script does the following:

1. **Fetches anime data**: Extracts the anime name and the number of episodes from the anime's main page on **AnimeFLV**.
2. **Fetches episode URLs**: Generates a list of URLs for each available episode.
3. **Fetches video servers**: For each episode, extracts available video servers and their codes.
4. **Uses concurrency**: The use of `ThreadPoolExecutor` enables efficient data fetching for all episodes concurrently.

## Requirements

To run this project, you need the following Python packages:

- `requests`
- `beautifulsoup4`
- `lxml` (optional, but recommended for improved performance with BeautifulSoup)
- `json`
- `re`
- `concurrent.futures` (included in Python 3.2 and later)
- `sys`

You can install the required packages using `pip`:

```bash
pip install requests beautifulsoup4 lxml
```
## Usage

### Running from the Command Line:

1. Clone this repository or download the `scraper.py` file.
2. Open a terminal and navigate to the directory where the file is located.
3. Run the script with the anime page URL from **AnimeFLV** as an argument:

   ```bash
   python scraper.py https://www3.animeflv.net/anime/steinsgate-0
   ```
## Output

The script will output a JSON object containing the video server information for each episode. The structure of the output is as follows:

### Example Output:

```json
{
  "1": {
    "Server1": "code1",
    "Server2": "code2"
  },
  "2": {
    "Server1": "code1",
    "Server2": "code2"
  },
  "3": {
    "Server1": "code1",
    "Server3": "code3"
  }
}
