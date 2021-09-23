import urllib.request
from os import remove
from shutil import copy


print("Checking for updates")
mainData = ""
with open("main.pyw", "r") as file:
    mainData = file.read()
urllib.request.urlretrieve("https://github.com/Owenknowsbest/Game-Launcher/raw/main/main.pyw", "temp")
with open("temp", "r") as file:
    data = file.read()
    if mainData != data:
        print("Updating main.pyw!")
        remove("main.pyw")
        copy("temp", "main.pyw")
remove("temp")
gameData = ""
with open("config.json", "r") as file:
    gameData = file.read()
urllib.request.urlretrieve("https://github.com/Owenknowsbest/Game-Launcher/raw/main/config.json", "temp")
with open("temp", "r") as file:
    data = file.read()
    if gameData != data:
        print("Updating config.json!")
        remove("config.json")
        copy("temp", "config.json")
remove("temp")
print("Finished!")
