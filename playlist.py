import os
from pytube import Playlist
from pytube import YouTube
from pytube import request

class youtube(Playlist):
    def __init__(self):
        self.playlist_url = input("Youtube Playlist url: ")
        self.download_path = input("Download Path: ")
        Playlist.__init__(self, self.playlist_url)

    def download_all(
        self, download_path=None, prefix_number=True,
        reverse_numbering=False,
    ):

        self.populate_video_urls()
        print(self.video_urls[0])
        if (download_path==None):
            playlist_folder_title = YouTube(self.video_urls[0]).title
            playlist_folder_list = str(playlist_folder_title).split()[:10]
            playlist_folder = '-'.join(playlist_folder_list)
            dir = os.path.dirname(__file__)
            folder_name = os.path.join(dir, playlist_folder)
            print("Folder Name: ",playlist_folder)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            download_path = folder_name

        #prefix_gen = self._path_num_prefix_generator(reverse_numbering)
        print("@@@@@@ Generating Youtube Playlist Streams to Download @@@@@")
        print("Download Path: ", download_path)
        print("Total Video Found: ", len(self.video_urls))
        item_count = 0;
        for link in self.video_urls:
            item_count += 1
            print(item_count)
            yt = YouTube(link)
            print("Downloading... : ", yt.title)
            # TODO: this should not be hardcoded to a single user's preference
            dl_stream = yt.streams.filter( res="360p", mime_type="video/mp4", progressive=True).first()
            if prefix_number:
                dl_stream.download(download_path)
            else:
                dl_stream.download(download_path)
            print("download completed: ", yt.title)


y = youtube()
y.download_all()
