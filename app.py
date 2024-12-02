import os
import platform
import subprocess
import time

from yt_dlp import YoutubeDL

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
    print('2. Download MP3')
    print('3. Exit\n')
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
        chosen_option = int(input('Choose an option: ').strip())

        if chosen_option == 1:
            start_download()

        elif chosen_option == 2:
            start_download(True)

        elif chosen_option == 3:
            finish_app()

        else:
            invalid_option()
    except ValueError:
        invalid_option()
def start_download(only_audio=False):
    playlist_url = input("Enter the url: ").strip()
    resolution = '720p'

    if not only_audio:
        resolutions = ["360p", "720p", "1080p"]
        resolution = input(f"Please select a resolution {resolutions}: ").strip()

    download(playlist_url, resolution, only_audio=only_audio)
def download(url, resolution='720p', only_audio=False):
    """
    Function to download all videos or audios from a playlist.
    :param resolution: Is the quality of the video
    :param url: URL of the YouTube playlist.
    :param only_audio: If True, downloads only the audios.
    """
    output=outputs_folder
    path_custom = '/%(playlist_title)s/' if 'playlist' in url else ''

    try:
        ydl_opts = {
            'outtmpl': f'{output}{path_custom}/%(title)s.%(ext)s',
            'format': f'bestvideo[height<={resolution.replace("p", "")}][ext=mp4]+bestaudio[ext=m4a]' if not only_audio else 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ] if only_audio else [],
            'merge_output_format': 'mp4',
            'ignoreerrors': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Playlist baixada com sucesso!")

        open_directory()
    except Exception as e:
        print(f"Erro ao baixar a playlist: {e}")
def open_directory():
    path = outputs_folder
    if platform.system() == "Windows":
        subprocess.run(["explorer", path])
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", path])
    else:
        print("\nSistema operacional não suportado.\n")

def main():
    os.system('clear')

    if not os.path.exists(outputs_folder):
        os.makedirs(outputs_folder)

    name_project()
    menu_options()
    choose_options()

if __name__ == '__main__':
    main()