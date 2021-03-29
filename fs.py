import dpath.util as filer #For accessing nested dictionaries using file path strings such as '/apps/helloworld.py'
from dpath.exceptions import PathNotFound
from prompt_toolkit import prompt
from os import listdir
from os.path import isfile
from os import system as hostcmd
from os import name as hostname

def clear():
    if hostname == "nt":
        hostcmd("cls")
    else:
        hostcmd("clear")

class filesystem: #The file system class
    
    def __init__(self):
        self.fs = {}
        self.cwd = "/"
        self.apps = []
        self.systemdirs = [
            "/apps"
            ]
    def formatpath(self, file):
        if not file.startswith("/"):
            if self.cwd == "/":
                file = self.cwd + file
            else:
                file = self.cwd + "/" + file
        file.replace("//", "/")
        return file
    def edit(self, file, val): #To easily edit files or folders
        filer.set(self.fs, self.formatpath(file), val)
    
    def new(self, file, val): #To easily edit files or folders
        filer.new(self.fs, self.formatpath(file), val)
        
    def read(self, file): #To get the stored value of a file or folder
        return filer.get(self.fs, self.formatpath(file))
    
    def delete(self, file):
        if self.cwd == file:
            print("Error: You are in this folder.")
        if file in self.systemdirs:
            print("Access denied: system directory")
            return
        try:
            filer.delete(self.fs, self.formatpath(file))
        except PathNotFound:
            print("Invalid file or folder")
    
    def move(self, file, newloc):
        if ("." in file) == ("." in newloc):
            file = self.formatpath(file)
            newloc = self.formatpath(newloc)
            try:
                filecont = self.read(file)
                self.new(newloc, filecont)
                self.delete(file)
            except KeyError:
                print("Error: file or path not found")
        else:
            print("Error: Can't convert file to folder and vice versa")
    
    def clone(self, file):
        try:
            file = self.formatpath(file)
            fold = "/".join(file.split("/")[:-1])
            if "." in file:
                filename = ".".join(file.split("/")[-1].split(".")[:-1])
                fnt = file.split("/")[-1].split(".")[-1]
                self.new(fold + "/" + filename + "-clone" + "." + fnt, self.read(file))
            else:
                self.new(file + "-clone", self.read(file))
                
        except:
            print("Error: File not found")
    
    def make(self, file): #To easily edit files or folders
        if "." in file:
            filer.new(self.fs, self.formatpath(file), "")
        else:
            filer.new(self.fs, self.formatpath(file), {})
    
    def cd(self, file):
        if file == "..":
            nwd = self.cwd
            nwd = nwd.split("/")
            del nwd[-1]
            nwd = "/".join(nwd)
            nwd = "/" + nwd
            nwd = nwd.replace("//", "/")
            self.cwd = nwd
            return
        file = self.formatpath(file)
        try:
            self.read(file)
            if "." in file:
                raise KeyError()
            self.cwd = file
            self.cwd = self.cwd.replace("//", "/") #just in case
        except KeyError:
            print("Invalid directory")
    
    def ls(self):
        for item in self.read(self.cwd).keys():
            print(item)
    
    def np(self, file):
        try:
            if not "." in file:
                raise KeyError
            text = self.read(file)
            clear()
            while True:
                print("Press ESC and then Enter to finish.")
                answer = prompt(
                    "", multiline=True, default=text)
                text = answer
                clear()
                while True:
                    print("Type 1 to save, 2 to keep editing, or 3 to cancel.")
                    option = input()
                    if option == "1":
                        self.edit(file, text)
                        clear()
                        return
                    elif option == "2":
                        clear()
                        break
                    elif option == "3":
                        clear()
                        return
                    else:
                        print("That's not a valid option.")
                        
        except KeyError:
            print("Error: File not found")
    
    def rename(self, file, newfile):
        try:
            content = self.read(file)
            self.delete(file)
            self.make(newfile)
            self.edit(newfile, content)
        except KeyError:
            print("Error: File not found")
    
    def readprint(self, file):
        try:
            print(self.read(file))
        except KeyError:
            print("Error: File not found")
    
    def updateapps(self): #To set up the apps
        apps = [f for f in listdir("apps")]
        for i in range(0, len(apps)):
            if apps[i] == "__pycache__":
                del apps[i]
        self.apps = apps
        for app in apps:
            self.new(("/apps/" + app.replace('.py', '.exe')), app)
