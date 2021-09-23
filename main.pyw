from tkinter import *
from tkinter import ttk
import zipfile
import urllib.request
from os import remove
from os import system
from os import chdir
from os.path import exists
from os.path import isdir
from os import getcwd
from shutil import rmtree
from shutil import copy
from shutil import copytree
import json


config = []
with open("config.json", "r") as file:
    config = json.load(file)


class GameTab(Frame):
    def __init__(self, master=None, game=None):
        super().__init__(master)
        self.TitleText = game["Display"]["Title"]
        self.DescText = game["Display"]["Description"]
        if "UseReadme" in game["Display"] and game["Display"]["UseReadme"]:
            read_me_data = urllib.request.urlopen(game["ReadmeURL"])
            if len(self.DescText) > 0:
                self.DescText += "\n\n-- READ ME --\n\n"
            self.DescText += read_me_data.read().decode('utf-8')
        self.GameData = game
        self.InstallStatus = False
        self.LauncherDir = getcwd()
        # Name, Description
        self.Title = Label(self, text=self.TitleText)
        self.Title.grid(row=0, column=0)
        self.Description = Text(self, width=40, height=10)
        self.Description.insert("1.0", self.DescText)
        self.Description.config(state=DISABLED)
        self.Description.grid(row=1, column=0, columnspan=3)
        # Update Button, Play Button
        self.UpdateButton = Button(self, text="Install", command=self.download_update)
        self.UpdateButton.grid(row=2, column=0)
        if not self.GameData["StartFile"]["NoRun"]:
            self.PlayButton = Button(self, text="Play", command=self.play)
            self.PlayButton.grid(row=2, column=2)
        # Uninstall Button
        self.UninstallButton = Button(self, text="Uninstall", command=self.uninstall)
        self.UninstallButton.grid(row=2, column=1)
        # Install Status
        self.InstallIndicator = Label(self)
        self.InstallIndicator.grid(row=0, column=1)
        # Delete Persistent Data
        self.DeletePersistentDataButton = Button(self, text="Delete Persistent Data",
                                                 command=self.remove_persistent_data)
        self.update_install_status()

    def download_update(self):
        if exists("Games/" + self.GameData["FileName"][:-4]):
            for file in self.GameData["Persistent"]:
                self.save_persistent_data(file)
            rmtree("Games/" + self.GameData["FileName"][:-4])
        urllib.request.urlretrieve(self.GameData["DownloadURL"], "Games/"+self.GameData["FileName"])
        with zipfile.ZipFile("Games/"+self.GameData["FileName"]) as zFile:
            zFile.extractall("Games/"+self.GameData["FileName"][:-4])
        remove("Games/"+self.GameData["FileName"])
        for file in self.GameData["Persistent"]:
            self.load_persistent_data(file)
        self.update_install_status()

    def play(self):
        if self.InstallStatus:
            chdir(f'Games/{self.GameData["FileName"][:-4]}')
            self.master.master.destroy()
            system(f'{self.GameData["StartFile"]["Use"]} {self.GameData["StartFile"]["FileName"]}')

    def uninstall(self):
        if self.InstallStatus:
            for file in self.GameData["Persistent"]:
                self.save_persistent_data(file)
            rmtree("Games/" + self.GameData["FileName"][:-4])
            self.update_install_status()

    def update_install_status(self):
        self.InstallStatus = exists("Games/"+self.GameData["FileName"][:-4])
        if self.InstallStatus:
            self.InstallIndicator.config(text="Installed")
            self.UpdateButton.config(text="Update")
            self.DeletePersistentDataButton.grid_forget()
        else:
            self.InstallIndicator.config(text="Uninstalled")
            self.UpdateButton.config(text="Install")
            if exists("Persistent Files/" + self.GameData["FileName"][:-4]):
                self.DeletePersistentDataButton.grid(row=0, column=2)

    def save_persistent_data(self, file):
        if not isdir("Games/" + self.GameData["FileName"][:-4] + "/" + file):
            copy("Games/" + self.GameData["FileName"][:-4] + "/" + file,
                 "Persistent Files/" + self.GameData["FileName"][:-4] + "/" + file)
        else:
            copytree("Games/" + self.GameData["FileName"][:-4] + "/" + file,
                     "Persistent Files/" + self.GameData["FileName"][:-4] + "/" + file)

    def load_persistent_data(self, file):
        if not exists("Persistent Files/" + self.GameData["FileName"][:-4] + "/" + file):
            return
        if not isdir("Persistent Files/" + self.GameData["FileName"][:-4] + "/" + file):
            remove("Games/" + self.GameData["FileName"][:-4] + "/" + file)
            copy("Persistent Files/" + self.GameData["FileName"][:-4] + "/" + file,
                 "Games/" + self.GameData["FileName"][:-4] + "/" + file)
            rmtree("Persistent Files/" + self.GameData["FileName"][:-4])
        else:
            rmtree("Games/" + self.GameData["FileName"][:-4] + "/" + file)
            copytree("Persistent Files/" + self.GameData["FileName"][:-4] + "/" + file,
                     "Games/" + self.GameData["FileName"][:-4] + "/" + file)
            rmtree("Persistent Files/" + self.GameData["FileName"][:-4])

    def remove_persistent_data(self):
        if not exists("Persistent Files/" + self.GameData["FileName"][:-4]):
            return
        rmtree("Persistent Files/" + self.GameData["FileName"][:-4])
        self.DeletePersistentDataButton.grid_forget()


class App(Tk):
    TabContents = []

    def __init__(self):
        super().__init__()
        self.Tabs = ttk.Notebook(self)
        self.Tabs.pack()
        self.initialize_tabs()
        self.mainloop()

    def initialize_tabs(self):
        for game in config:
            if "Ignore" in game and game["Ignore"]:
                continue
            game_tab = GameTab(self.Tabs, game)
            self.TabContents.append(game_tab)
            self.Tabs.add(game_tab, text=game_tab.TitleText)


app = App()
