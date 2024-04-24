from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import moviepy.editor as mp
import os

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_link.delete(0, END)
    folder_link.insert(0, folder_selected)

def download_audio():
    download_status.config(text="Downloading...")
    root.update()

    video_url = ytlink.get()
    save_path = folder_link.get()
    os.makedirs(save_path, exist_ok=True)

    yt = YouTube(video_url)

    # Filter the streams to get the audio-only streams
    audio_streams = yt.streams.filter(only_audio=True)

    # Select the first available audio stream
    selected_audio_stream = audio_streams.first()

    if selected_audio_stream:
        # Download the selected audio stream
        audio_filename = yt.title + ".mp4"
        audio_path = os.path.join(save_path, audio_filename)
        selected_audio_stream.download(output_path=save_path, filename=audio_filename)

        # Convert the downloaded audio to MP3 using moviepy
        try:
            audio = mp.AudioFileClip(audio_path)
            audio.write_audiofile(os.path.join(save_path, yt.title + ".mp3"))
            audio.close()
            os.remove(audio_path)  # Remove the temporary audio file
            download_status.config(text="Downloaded successfully!")
        except Exception as e:
            download_status.config(text="Error converting audio to MP3: {}".format(e))
            if os.path.exists(audio_path):
                os.remove(audio_path)
    else:
        download_status.config(text="No suitable audio stream found.")

    root.update()


root = Tk()
root.title("Aymen Trabelsi - MR ROBOT")
root.geometry("600x320")

# Load the YouTube logo image and make it smaller
ytlogo = PhotoImage(file="Logoooo.png").subsample(4)
ytitle = Label(root, image=ytlogo)
ytitle.place(relx=0.5, rely=0.2, anchor="center")

# YouTube Link Label and Entry widget
yt_label = Label(root, text="YouTube Link")
yt_label.place(x=25, y=150)

ytlink = Entry(root, width=50)
ytlink.place(x=125, y=150)

# Download folder Label and Entry widget
folder_label = Label(root, text="Download folder")
folder_label.place(x=25, y=180)

folder_link = Entry(root, width=40)
folder_link.place(x=125, y=180)

# Browse Button
browse = Button(root, text="Browse", command=browse_folder)
browse.place(x=380, y=175)

# Download MP3 Button
download_mp3 = Button(root, text="Download", command=download_audio)
download_mp3.place(x=280, y=220)

# Download status label
download_status = Label(root, text="", fg="blue")
download_status.place(x=10, y=290)

root.mainloop()
