from pytube.cli import on_progress
from pytube import YouTube
from pytube import Playlist
from pytube.extract import playlist_id
# from pytube.extract import video_id
import os

def path_creator():
    #location where file will be downloaded
    des_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "Youtube")
    if os.path.exists(des_path):
        return des_path

    else:
        #Create Youtube folder on desktop if it does not exist
        os.makedirs(des_path, exist_ok=True) 
        return des_path



def is_playlist(url):
    """
    url: str
    Return: True(Bolean) if url is of a playlist
    """
    try:
        pl_id = playlist_id(url)
        return True

    except KeyError: 
        return False


def youtube_url(url):
    """
    url: str
    Return: A list of video urls in a playlist
    """   
    playlist = Playlist(url)
    return playlist.video_urls

    
def downloader(url):
    """
    url: str
    Return: None
    Download video of resolution 720p or highest available resolution 
    """   
    try:
        yt_obj = YouTube(url, on_progress_callback=on_progress)
        title = yt_obj.title
        print(f"\n{title} is downloading...")
        stream_obj = yt_obj.streams

        try:
            selected_stream = stream_obj.filter(progressive=True, resolution="720p")[0]
            
        except:
            selected_stream = stream_obj.get_highest_resolution()
            
        finally:
            selected_stream.download(output_path=path_creator())

    except Exception as err:
        return err

    else:
        return f"{title} downloaded\n"


# main driver
if __name__ == '__main__':

    print("Initilizing the script...\n")
    url = input("Enter the url of the youtube playlist or video:\n")
    while True:
        
        if is_playlist(url):
            for vid_url in youtube_url(url):
                print(downloader(vid_url))
        else:
            print(downloader(url))

        print(r"NOTE: You can find your downloads in C:\Users\DRB\Desktop\Youtube.\n")

        command = input("Press any key to close program and 'N' to continue more downloading: ")
        if "N" != command.upper():
            break
        url = input("\nEnter the url of the youtube playlist or video:\n")
        # print("\n====== Done - Check Download Folder =======")
