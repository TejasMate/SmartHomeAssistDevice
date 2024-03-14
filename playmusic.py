import yt_dlp
import os
from concurrent.futures import ThreadPoolExecutor


def download_audio(query):
    # YouTube downloader options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Create a yt-dlp instance
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Search for the video
        info = ydl.extract_info(f"ytsearch:{query}", download=False)

        if not info['entries']:
            print(f"No results found for '{query}'")
            return

        # Get the first search result
        video_info = info['entries'][0]
        video_url = video_info['webpage_url']
        video_title = video_info['title']

        print(f"Downloading '{video_title}'...")

        # Download the audio
        ydl.download([video_url])

        # Get the downloaded audio file name
        audio_file = f"{video_title}.mp3"

        # Get the current working directory
        cwd = os.getcwd()

        # Print the file path
        print(f"Audio saved to: {os.path.join(cwd, audio_file)}")


def main(query):
    import time
    start = time.time()

    # # Get the song name and artist
    # song_name = "memories like this"
    # artist_name = "the afters"

    # # Search query
    # query = f"{song_name} {artist_name}"
    
    # Use multithreading to download multiple audio files concurrently
    with ThreadPoolExecutor() as executor:
        executor.submit(download_audio, query)
        
    end = time.time()
    print(end - start)

    

# if __name__ == "__main__":
#   main()/