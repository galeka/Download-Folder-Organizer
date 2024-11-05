#!/usr/bin/env python3
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from locations import *

class ShiftingFiles(FileSystemEventHandler):
    """
    This class allows us to override the FileSystemEventHandler methods.
    """
    download_folders = ["photos", "documents", "folders", "music", "zipFiles",
                        "videos", "others", ".DS_Store", "code"]

    def on_modified(self, event):
        self.check_if_downloading()
        existing_files = os.listdir(download_location)
        if existing_files != self.download_folders:
            self.shift()

    def shift(self):
        """Shift all files from one location to another."""
        try:
            existing_files = os.listdir(download_location)
            for file_name in existing_files:
                if file_name not in folders:
                    if file_name != ".DS_Store":
                        transfer_folder = self.which_location(file_name)
                        os.rename(download_location + "/" + file_name,
                                  transfer_folder + "/" + file_name)
        except FileNotFoundError:
            print("Error Occurred: Some thing went wrong!")
            print("Please run the script again, if the script stops")
            exit()

    def which_location(self, file_name):
        """Decide what location is suitable for a kind of file."""
        if file_name.find(".") != -1:
            temp = file_name.split(".")
            file_ext = temp[-1].lower()
            if file_ext in ["jpg", "tiff", "gif", "png", "raw", "jpeg", "CR2", "HEIC"]:
                return photo_location
            if file_ext in ["mp3", "wav"]:
                return music_location
            if file_ext in ["pdf", "txt", "docs", "docx", "ppt", "pptx"]:
                return document_location
            if file_ext == "zip":
                return zipfile_location
            if file_ext in ["mp4", "avi", "mov", "wmv", "flv"]:
                return video_location
            if file_ext in ["py", "js", "ipynb", "java", "ts"]:
                return code_location
            return other_location
        else:
            if os.path.isdir(os.path.join(download_location, file_name)):
                return folder_location
            return other_location

    def check_if_downloading(self):
        """Check if there is any downloading at the moment."""
        new_files = os.listdir(download_location)
        for file_name in new_files:
            temp = file_name.split(".")
            file_ext = temp[-1]
            if ".com.google.Chrome" not in file_name:
                if "crdownload" in file_ext or "download" in file_ext:
                    time.sleep(60)
                    self.check_if_downloading()
            else:
                time.sleep(5)
                self.check_if_downloading()
        return None

def create_folders():
    """Create necessary folders in the download location."""
    for folder_name in folders:
        folder_path = os.path.join(download_location, folder_name)
        os.makedirs(folder_path, exist_ok=True)  # Creates the directory if it doesn't exist

if __name__ == "__main__":
    folders = ["photos", "documents", "folders", "music", "zipFiles", "videos",
               "others", "code"]  # Folders to create
    create_folders()  # Create necessary folders
    ShiftingFiles().shift()  # Shift files as soon as the program is run

    # Set up the watchdog observer
    event_handler = ShiftingFiles()
    observer = Observer()
    observer.schedule(event_handler, download_location, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

