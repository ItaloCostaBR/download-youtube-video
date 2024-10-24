import os
import re
import time

from pytube import Playlist, YouTube
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm import tqdm

# Comment above line and uncomment below line if you're using pytubefix
# from pytubefix import Playlist, YouTube
outputs_folder = 'outputs'

def name_project():
    print("""
            ██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗██╗░░░░░░█████╗░░█████╗░██████╗░
            ██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║██║░░░░░██╔══██╗██╔══██╗██╔══██╗
            ██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║██║░░░░░██║░░██║███████║██║░░██║
            ██║░░██║██║░░██║░░████╔═████║░██║╚████║██║░░░░░██║░░██║██╔══██║██║░░██║
            ██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║███████╗╚█████╔╝██║░░██║██████╔╝
            ╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝╚══════╝░╚════╝░╚═╝░░╚═╝╚═════╝░
██╗░░░██╗░█████╗░██╗░░░██╗████████╗██╗░░░██╗██████╗░███████╗░░░░░░░░██╗░░░██╗██╗██████╗░███████╗░█████╗░
╚██╗░██╔╝██╔══██╗██║░░░██║╚══██╔══╝██║░░░██║██╔══██╗██╔════╝░░░░░░░░██║░░░██║██║██╔══██╗██╔════╝██╔══██╗
░╚████╔╝░██║░░██║██║░░░██║░░░██║░░░██║░░░██║██████╦╝█████╗░░░░░░░░░░╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║
░░╚██╔╝░░██║░░██║██║░░░██║░░░██║░░░██║░░░██║██╔══██╗██╔══╝░░░░░░░░░░░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║
░░░██║░░░╚█████╔╝╚██████╔╝░░░██║░░░╚██████╔╝██████╦╝███████╗░░░░░░░░░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝
░░░╚═╝░░░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚═════╝░╚═════╝░╚══════╝░░░░░░░░░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░
    """)
def text_start_fn(text):
    os.system('clear')
    print("""*******************************""")
    print(f'{text}')
    print("""*******************************""")
def menu_options():
    print('\n1. Download Video')
    print('2. Download Playlist')
    print('3. Convert to mp3')
    print('4. Exit\n')
def invalid_option():
    print('Invalid option! Try entering the option number.\nRestarting system...')
    time.sleep(2)
    main()
def finish_app():
    print("""
░██████╗██╗░░██╗██╗░░░██╗████████╗████████╗██╗███╗░░██╗░██████╗░██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗
██╔════╝██║░░██║██║░░░██║╚══██╔══╝╚══██╔══╝██║████╗░██║██╔════╝░██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║
╚█████╗░███████║██║░░░██║░░░██║░░░░░░██║░░░██║██╔██╗██║██║░░██╗░██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║
░╚═══██╗██╔══██║██║░░░██║░░░██║░░░░░░██║░░░██║██║╚████║██║░░╚██╗██║░░██║██║░░██║░░████╔═████║░██║╚████║
██████╔╝██║░░██║╚██████╔╝░░░██║░░░░░░██║░░░██║██║░╚███║╚██████╔╝██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║
╚═════╝░╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝
    """)
def choose_options():
    try:
        chosen_option = int(input('Choose an option: '))

        if chosen_option == 1:
            print('1. Download Video')

        elif chosen_option == 2:
            start_download_playlist()

        elif chosen_option == 3:
            print('3. Convert to mp3')

        elif chosen_option == 4:
            finish_app()

        else:
            invalid_option()
    except ValueError:
        invalid_option()

def start_download_playlist():
    playlist_url = input("Enter the playlist url: ")
    resolutions = ["240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
    resolution = input(f"Please select a resolution {resolutions}: ")
    download_playlist(playlist_url, resolution)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def download_with_retries(stream, filename):
    stream.download(filename=filename)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    print(f"Downloading... {percentage_of_completion:.2f}% complete", end="\r")

def download_playlist(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    playlist_name = sanitize_filename(re.sub(r'\W+', '-', playlist.title))

    if not os.path.exists(os.path.join(outputs_folder, playlist_name)):
        os.mkdir(os.path.join(outputs_folder, playlist_name))

    for index, video in enumerate(tqdm(playlist.videos, desc="Downloading playlist", unit="video"), start=1):
        yt = YouTube(video.watch_url, on_progress_callback=progress_function)
        video_streams = yt.streams.filter(res=resolution)

        video_filename = sanitize_filename(f"{index}. {yt.title}.mp4")
        video_path = os.path.join(playlist_name, video_filename)

        if os.path.exists(video_path):
            print(f"{video_filename} already exists")
            continue

        if not video_streams:
            highest_resolution_stream = yt.streams.get_highest_resolution()
            video_name = sanitize_filename(highest_resolution_stream.default_filename)
            print(f"Downloading {video_name} in {highest_resolution_stream.resolution}")
            download_with_retries(highest_resolution_stream, video_path)
        else:
            video_stream = video_streams.first()
            video_name = sanitize_filename(video_stream.default_filename)
            print(f"Downloading video for {video_name} in {resolution}")
            download_with_retries(video_stream, "video.mp4")

            audio_stream = yt.streams.get_audio_only()
            print(f"Downloading audio for {video_name}")
            download_with_retries(audio_stream, "audio.mp4")

            os.system("ffmpeg -y -i video.mp4 -i audio.mp4 -c:v copy -c:a aac final.mp4 -loglevel quiet -stats")
            os.rename("final.mp4", video_path)
            os.remove("video.mp4")
            os.remove("audio.mp4")

        print("----------------------------------")

def main():
    os.system('clear')
    name_project()
    menu_options()
    choose_options()

if __name__ == '__main__':
    main()