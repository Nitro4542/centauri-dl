import os
import tkinter
from tkinter import messagebox
import customtkinter
import downloader as dl

class ChooseAudioOrVideoFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.radiobutton_var = tkinter.IntVar(value=0)

        self.title = customtkinter.CTkLabel(self, text="Choose what to download:", justify="center")
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.radiobutton_video = customtkinter.CTkRadioButton(self, text="Video", value=0, variable=self.radiobutton_var)
        self.radiobutton_video.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.radiobutton_audio = customtkinter.CTkRadioButton(self, text="Audio", value=1, variable=self.radiobutton_var)
        self.radiobutton_audio.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def make_file_extensions(self):
        if self.radiobutton_var.get() == 0:
            return ["MPEG-4 (.mp4)", "QuickTime (.mov)", "Matroska (.mkv)", "WEBM (.webm)"]
        else:
            return ["MPEG layer 3 (.mp3)", "Waveform (.wav)", "Free Lossless Audio Codec (.flac)", "Vorbis (.ogg)"]


class OutputOptionsFrame(customtkinter.CTkFrame):
    def __init__(self, master, main_object, choose_audio_or_video_object):
        super().__init__(master)

        self.choose_audio_or_video_object = choose_audio_or_video_object
        self.choose_audio_or_video_object_extensions = choose_audio_or_video_object.make_file_extensions()

        self.main_object = main_object

        self.downloader = None
        self.output_path = None

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.title = customtkinter.CTkLabel(self, text="Choose your output options:", justify="center")
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        self.output_button = customtkinter.CTkButton(self, text="Choose output path", command=lambda: self.output_folder_file_dialog())
        self.output_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.download_button = customtkinter.CTkButton(self, text="Start download", command=lambda: self.start_download(self.main_object))
        self.download_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def output_folder_file_dialog(self):
        self.output_path = customtkinter.filedialog.askdirectory()

    def update_choose_audio_or_video_extensions(self):
        self.choose_audio_or_video_object_extensions = self.choose_audio_or_video_object.make_file_extensions()

    def convert_output_format(self):
        self.update_choose_audio_or_video_extensions()
        if self.choose_audio_or_video_object_extensions[0] == "MPEG-4 (.mp4)":
            return 1
        else:
            return 0

    def start_download(self, main_object):
        self.downloader = dl.Downloader(main_object.url_input.get(), self.convert_output_format(), self.output_path)

        print(f"URL entered: {main_object.url_input.get()}")
        print(f"Check URL result: {self.downloader.check_url()}")
        print(f"Output path: {self.output_path}")

        if main_object.url_input.get() and self.downloader.check_url() == 0:
            if self.output_path and os.path.exists(self.output_path):
                self.downloader.download()
            else:
                messagebox.showerror("Error", "Please select a valid output path")
        else:
            messagebox.showerror("Error", "Please select a valid URL")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x210")
        self.title("centauri")

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.url_input = customtkinter.CTkEntry(self, placeholder_text="Enter URL")
        self.url_input.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="new")

        self.choose_audio_or_video_frame = ChooseAudioOrVideoFrame(self)
        self.choose_audio_or_video_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

        self.output_options_frame = OutputOptionsFrame(self, self, self.choose_audio_or_video_frame)
        self.output_options_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
