import os
import urllib.request
from os import path

import pytube
import PySimpleGUI as gui
from PIL import Image
from pytube.exceptions import RegexMatchError

def download_thumbnail(image_url):
    file_name = "temp_thumbnail"
    urllib.request.urlretrieve(image_url, file_name)
    im = Image.open(file_name).convert("RGB")
    im.thumbnail((200, 100))
    im.save(file_name + ".png", "png")
    os.remove("temp_thumbnail")

if __name__ == '__main__':
    layout = [
        [
            gui.Column([
                [
                    gui.Text("URL:", size=(10, 1)),
                    gui.In(size=(40, 1), key="-URL-"),
                    gui.Button("Retrieve video", size=(10, 1), key="-RETRIEVE-")
                ],
                [
                    gui.Text("Save location:", size=(10, 1)),
                    gui.In(size=(40, 1), key="-SAVEDIR-"),
                    gui.FolderBrowse(size=(10, 1))
                ],
                [
                    gui.Image(size=(100, 100), pad=(155, 10), key="-THUMBNAIL-"),
                ],
                [
                    gui.Text("", size=(40, 1), pad=(82, 10), justification="center", key="-TITLE-")
                ],
                [
                    gui.Button("Download", size=(20, 1), pad=(160, 20), key="-DOWNLOAD-", disabled=True)
                ]
            ])
        ]
    ]

    window = gui.Window("Youtube Downloader", layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == "-RETRIEVE-":
            try:
                youtube = pytube.YouTube(values["-URL-"])
                window.find_element("-DOWNLOAD-").Update(disabled=False)
                window.find_element("-TITLE-").Update(youtube.title.title())
                download_thumbnail(youtube.thumbnail_url)
                window.find_element("-THUMBNAIL-").Update(filename="./temp_thumbnail.png")
            except RegexMatchError:
                window.find_element("-DOWNLOAD-").Update(disabled=True)
                print("ERROR: URL not found")

        if event == "-DOWNLOAD-":
            try:
                if os.path.isdir(values["-SAVEDIR-"]):
                    savedir = values["-SAVEDIR-"]
                else:
                    raise NameError
                video = youtube.streams.filter(progressive=True).first().download(savedir)
                print("Video Downloaded!")
            except NameError:
                print("ERROR: Directory does not exist")

    if path.exists("./temp_thumbnail.png"):
        os.remove("./temp_thumbnail.png")