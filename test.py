"""
Pytube GUI
written by Matthew Reid

This is a simple graphical user interface for the pytube module using tkinter.
While pytube is very powerful, this GUI makes use of only a few functions to make it simple for users.
There are 2 import options; link or txt file containing links.
If you are using a txt file with links for batch processing, there must be a separate link on each new line and no blank lines in the file.
The download options are for audio only, best progressive (video with audio) which is 360p, and best video.
All files will be downloaded as mp4.
There is also an option to select the download folder.

The progress indicator shows the user when the program is working to get the stream information, which file it is up to, and the progress on that file.

I hope you enjoy using this GUI.
If you have any questions, please email me: m.reid854@gmail.com

A huge thanks to the creators of pytube.
"""
from pytube import request
from pytube.__main__ import YouTube
import pytube
import math
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, StringVar, IntVar, Entry
import re
import time
import os

# GUI SECTION###########################################################################################################
def create_GUI_layout(root):

    def change_folder():
        out_dir = filedialog.askdirectory(initialdir="/", parent=root)
        folder_text.set(out_dir)

    def select_file():
        out_link = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        out_link_text.set(out_link)
        # print(out_link)

    def commence_download_actions():
        # extract the inputs from the dialogs and checkboxes
        out_link = link_e.get()
        out_dir = out_e.get()
        audio = audio_var.get()
        video = video_var.get()
        video_only = video_only_var.get()
        #do the download
        conduct_download(out_link, out_dir, audio, video, video_only)

    def show_help():
        messagebox.showinfo("How to use the YouTube Plus Downloader",
                            'Welcome to the YouTube Plus Downloader Graphical User Interface.\n\n'
                            'You have 3 options to import YouTube stream information.\n\n 1. You can either paste Youtube '
                            'video link \n 2. You can either paste YouTube Playlist link \n 3. You can '
                            'select a txt file containing links. If you are using a txt file with links (referred '
                            'to as batch processing), then there must be a separate link on each new line and no blank '
                            'lines in the file or an error will occur.\n\n The download options are for audio only, best '
                            'progressive (video with audio) which is 360p, and best video. All files will be downloaded'
                            ' as mp4.\nThere is also an option to select the download folder, with the default location'
                            ' being the desktop. Once you start the download, the progress indicator will show when the'
                            ' program is working to get the stream information, which file it is up to, and the '
                            'progress on that file.\n\n YouTube Plus Downloader is a much more powerful module than this GUI allows, '
                            'however the GUI is intended to make some of the more common functions much easier to use.'
                            '\n\n This GUI was written by Shapon Pal from Bangladesh'
                            '\n To Use Web base service visit: http://youtubeplusdownloader.com')

    # Main title label
    title = tk.Label(root, text="YouTube Plus Downloader", font=("Purisa", 30))
    title.place(x=15, y=5)

    # Shop help button
    show_help_file_button = tk.Button(root, text="Show help", font=("Purisa", 10),command=show_help)
    show_help_file_button.place(x=620, y=15)

    # Label for Youtube link or batch folder
    Link_label = tk.Label(root, text="Paste YouTube Video link OR YouTube Playlist Link OR Select .txt file to batch process", font=("Purisa", 10))
    Link_label.place(x=15, y=60)

    out_link_text = StringVar()
    link_e = Entry(root, width=100, textvariable=out_link_text) #textbox for user entry
    link_e.pack()
    link_e.focus_set()  # moves the keyboard input to the textbox
    link_e.place(x=15,y=80)

    select_txt_file_button = tk.Button(root, text="Select .txt file to batch process", font=("Purisa", 10), command=select_file)
    select_txt_file_button.place(x=15, y=100)

    #audio and video checkboxes
    type_label = tk.Label(root, text="Select what you want to download from each YouTube link:", font=("Purisa", 10))
    type_label.place(x=15, y=140)

    audio_var = IntVar()
    type_button_audio = tk.Checkbutton(root, text="Best Audio", font=("Purisa", 10), variable=audio_var)
    type_button_audio.place(x=15, y=160)

    video_var = IntVar()
    type_button_video = tk.Checkbutton(root, text="Video 360p (with sound)", font=("Purisa", 10), variable=video_var)
    type_button_video.place(x=110, y=160)

    video_only_var = IntVar()
    type_button_video_only = tk.Checkbutton(root, text="Best Video (no sound)", font=("Purisa", 10), variable=video_only_var)
    type_button_video_only.place(x=280, y=160)

    #output folder selection
    output_folder_label = tk.Label(root, text="Select your output folder:", font=("Purisa", 10))
    output_folder_label.place(x=15, y=200)

    folder_text = StringVar()
    out_e = Entry(root, width=100, textvariable=folder_text)
    desktop_addr = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') #gets the address of the user's desktop
    folder_text.set(desktop_addr)
    out_e.pack()
    out_e.place(x=15,y=220)

    change_folder_button = tk.Button(root,text="Select Folder",font=("Purisa", 10),command=change_folder)
    change_folder_button.place(x=15, y=241)

    # download button - triggers data extraction and download actions
    download_button = tk.Button(root, text="Start Download", font=("Purisa", 20), command=commence_download_actions)
    download_button.place(x=15, y=290)

    # Author label
    title = tk.Label(root, text="Develop By: Shapon Pal", font=("Purisa", 20))
    title.place(x=380, y=340)


# DOWNLOAD SECTION######################################################################################################
def conduct_download(out_link,out_dir, audio, video, video_only):
    start = time.time()

    # create input warnings
    if len(out_link) == 0:
        messagebox.showinfo("Warning", 'You have not provided a link or a .txt file to process for download.\nPlease paste in a YouTube link or select a .txt file containing at least one YouTube link to download')
    elif audio + video + video_only == 0:
        messagebox.showinfo("Warning", 'You have not selected a file type to download.\nPlease tick at least one of the file types to download')

    # proceed if no input warnings are required
    else:
        print("File or link being used: ", out_link)
        print("Export directory: ", out_dir)

        # Use regular expressions to check if the link is a txt document and process the contents into a list
        pattern = r"txt$"
        playlist_id = out_link.split('&list=')[1]

        # this section will process txt files containing YouTube links
        if re.findall(pattern, out_link): # looks for the "txt" at the end and if found it treats it as a file
            file = open(out_link)
            content = file.readlines()
            links_processed = [x.strip() for x in content]  # remove whitespace characters like `\n` at the end of each line
            file.close()

            number_of_links = len(links_processed)
            total_items_to_download = (audio + video + video_only) * number_of_links

            each_link_count = 0
            for each_link in links_processed:
                print("Attempting to download:", each_link)

                fetching_label = tk.Label(root, text="Getting stream info (takes 10 sec)", font=("Purisa", 20))
                fetching_label.place(x=260, y=250)
                canvas.update_idletasks()

                yt = pytube.YouTube(each_link) # this link takes around 10 seconds due to the need to contact YouTube for stream info
                yt.register_on_progress_callback(show_progress)  # set the on_progress_callback to run the show_progress function at each chunk

                stream = []
                if audio == 1:
                    all_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').all()
                    stream.append(all_audio_streams[0])
                if video == 1:
                    all_video_streams = yt.streams.filter(res="360p", mime_type="video/mp4", progressive=True).all()
                    stream.append(all_video_streams[0])
                if video_only == 1:
                    all_video_only_streams = yt.streams.filter(subtype='mp4', only_video=True).order_by('resolution').all()
                    stream.append(all_video_only_streams[0])

                finish = time.time()
                print("Current Runtime:", finish - start, "seconds")
                fetching_label.destroy()
                canvas.update() # need to use canvas.update to destroy a canvas object. canvas.update_idletasks will not work

                for item in stream:
                    each_link_count += 1
                    print("Downloading:",item)
                    items_label = tk.Label(root, text="Downloading file " + str(each_link_count) + " of " + str(total_items_to_download), font=("Purisa", 14))
                    items_label.place(x=260, y=290)
                    canvas.update_idletasks()

                    #create a different filename for audio, progressive, and video only so that files don't get overwritten with the same name
                    if item.includes_audio_track is False and item.includes_video_track is True:
                        item_type = "video (no sound)"
                    elif item.includes_audio_track is True and item.includes_video_track is True:
                        item_type = "video"
                    elif item.includes_audio_track is True and item.includes_video_track is False:
                        item_type = "audio"
                    else:
                        item_type = ""  # this line should never eventuate
                    filename = str(item.default_filename)+" - "+item_type

                    item.download(out_dir, filename)  # this does the actual download
                    print("\nDownload complete")
                    finish = time.time()
                    print("Current Runtime:", finish - start, "seconds")

        # Youtube Playlist :: this section will process YouTube playlist
        elif ('watch?v=' in out_link) and len(playlist_id) > 16:
            playlist_url = out_link
            video_urls = []

            if 'watch?v=' in playlist_url:  # Make Youtube link in desired format
                base_url = 'https://www.youtube.com/playlist?list='
                playlist_code = playlist_url.split('&list=')[1]
                print("code >", playlist_code)
                playlist_url = base_url + playlist_code

            print("link: ", playlist_url)

            # Parse the video links from the page source, extracts and returns the /watch?v= part from video link href It's an alternative for BeautifulSoup :return: list
            url = playlist_url
            req = request.get(url)

            # split the page source by line and process each line
            content = [x for x in req.split('\n') if 'pl-video-title-link' in x]
            link_list = [x.split('href="', 1)[1].split('&', 1)[0] for x in
                         content]  # all Youtube Playlist video link : list
            print("Split Link: ", link_list)

            # Construct complete links of all the videos in playlist and populate video_urls list :return: urls -> string
            base_url = 'https://www.youtube.com'
            # populate_video_urls
            for video_id in link_list:
                complete_url = base_url + video_id
                video_urls.append(complete_url)
                links_processed = video_urls
            print('playlist -------',links_processed)

            # Start Download
            number_of_links = len(links_processed)
            total_items_to_download = (audio + video + video_only) * number_of_links

            each_link_count = 0
            for each_link in links_processed:
                print("Attempting to download:", each_link)

                fetching_label = tk.Label(root, text="Getting stream info (takes 10 sec)", font=("Purisa", 20))
                fetching_label.place(x=260, y=250)
                canvas.update_idletasks()

                yt = pytube.YouTube(
                    each_link)  # this link takes around 10 seconds due to the need to contact YouTube for stream info
                yt.register_on_progress_callback(
                    show_progress)  # set the on_progress_callback to run the show_progress function at each chunk

                stream = []
                if audio == 1:
                    all_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').all()
                    stream.append(all_audio_streams[0])
                if video == 1:
                    all_video_streams = yt.streams.filter(res="360p", mime_type="video/mp4", progressive=True).all()
                    stream.append(all_video_streams[0])
                if video_only == 1:
                    all_video_only_streams = yt.streams.filter(subtype='mp4', only_video=True).order_by(
                        'resolution').all()
                    stream.append(all_video_only_streams[0])

                finish = time.time()
                print("Current Runtime:", finish - start, "seconds")
                fetching_label.destroy()
                canvas.update()  # need to use canvas.update to destroy a canvas object. canvas.update_idletasks will not work

                for item in stream:
                    each_link_count += 1
                    print("Downloading:", item)
                    items_label = tk.Label(root, text="Downloading file " + str(each_link_count) + " of " + str(
                        total_items_to_download), font=("Purisa", 14))
                    items_label.place(x=260, y=290)
                    canvas.update_idletasks()

                    # create a different filename for audio, progressive, and video only so that files don't get overwritten with the same name
                    if item.includes_audio_track is False and item.includes_video_track is True:
                        item_type = "video (no sound)"
                    elif item.includes_audio_track is True and item.includes_video_track is True:
                        item_type = "video"
                    elif item.includes_audio_track is True and item.includes_video_track is False:
                        item_type = "audio"
                    else:
                        item_type = ""  # this line should never eventuate
                    filename = str(item.default_filename) + " - " + item_type

                    item.download(out_dir, filename)  # this does the actual download
                    print("\nDownload complete")
                    finish = time.time()
                    print("Current Runtime:", finish - start, "seconds")
            # End Download

        # Youtube Video Link :: this section will process YouTube video link
        else:   # this section will process the single link
            print("Attempting to download:", out_link)
            each_link_count = 0
            total_items_to_download = (audio + video + video_only)

            fetching_label = tk.Label(root, text="Getting stream info (takes 10 sec)", font=("Purisa", 14))
            fetching_label.place(x=260, y=250)
            canvas.update_idletasks()

            yt = pytube.YouTube(out_link) # this link takes around 10 seconds due to the need to contact YouTube for stream info
            yt.register_on_progress_callback(show_progress)  # set the on_progress_callback to run the show_progress function at each chunk

            stream = []
            if audio == 1:
                all_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').all()
                stream.append(all_audio_streams[0])
            if video == 1:
                all_video_streams = yt.streams.filter(res="360p", mime_type="video/mp4", progressive=True).all()
                stream.append(all_video_streams[0])
            if video_only == 1:
                all_video_only_streams = yt.streams.filter(subtype='mp4', only_video=True).order_by('resolution').all()
                stream.append(all_video_only_streams[0])

            finish = time.time()
            print("Current Runtime:", finish - start, "seconds")
            fetching_label.destroy()
            canvas.update()  # need to use canvas.update to destroy a canvas object. canvas.update_idletasks will not work

            for item in stream:
                each_link_count += 1
                print("Downloading:", item)
                items_label = tk.Label(root, text="Downloading file " + str(each_link_count) + " of " + str(total_items_to_download), font=("Purisa", 14))
                items_label.place(x=260, y=290)
                canvas.update_idletasks()

                # create a different filename for audio, progressive, and video only so that files don't get overwritten with the same name
                if item.includes_audio_track is False and item.includes_video_track is True:
                    item_type = "video (no sound)"
                elif item.includes_audio_track is True and item.includes_video_track is True:
                    item_type = "video"
                elif item.includes_audio_track is True and item.includes_video_track is False:
                    item_type = "audio"
                else:
                    item_type = ""  # this line should never eventuate
                filename = str(item.default_filename) + " - " + item_type

                item.download(out_dir, filename)
                print("\nDownload complete")
                finish = time.time()
                print("Current Runtime:", finish - start, "seconds")

def show_progress(stream, chunk, file_handle, bytes_remaining):
    bytes_downloaded = file_handle.tell()
    total_bytes = bytes_remaining + bytes_downloaded
    percent_downloaded = math.floor((bytes_downloaded / total_bytes)*100)
    print('\rProgress: '+str(percent_downloaded)+' %',end="")

    progress_label = tk.Label(root, text="Progress: " + str(percent_downloaded) + "%    ", font=("Purisa", 14))
    progress_label.place(x=260, y=320)
    canvas.update_idletasks()

# this is the initialising action for the tkinter canvas
root = tk.Tk()
root.title('Youtube Video Downloader by shapon')
canvas = Canvas(root, width=700, height=380)
canvas.pack()
create_GUI_layout(root)
root.mainloop()
