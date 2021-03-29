"""
PyrOS
By Boyne G.

todo list:
* Add more stuff to the app API
* Add app installer with app server
"""

print("Starting up...")

import time
import random
import sys
import json
import os
from os import system as hostcmd
from os import name as hostname
from colorama import Fore, Back
from os.path import isfile
from os import listdir
import colorama
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from importlib import import_module as imp

colorama.init()

sys.path.insert(0, './apps')

def clear():
    if hostname == "nt":
        hostcmd("cls")
    else:
        hostcmd("clear")

clear()

version = "1.0.0"
quotes = [
    "Better than Windows.",
    "Powered by you (you wish).",
    "Ohhh yeaaaaah.",
    "In the event of a fatal error, it's your fault.",
    "Pronounced 'pie row ess'.",
    "Like GLaDOS's twin.",
    "Pyro + OS = PyrOS.",
    "The Py in PyrOS is for Python."
    ]
clear()
startup = f"""{Fore.RED}
  _____                   ____    _____ 
 |  __ \                 / __ \  / ____|
 | |__) | _   _   _ __  | |  | | | (___  
 |  ___/ | | | | |  __| | |  | | \ ___ \ 
 | |     | |_| | | |    | |__| |  ____) |
 |_|      \__  | |_|     \____/  |_____/ 
           __/ |                   
          |___/
"""
startup = startup.splitlines()
for line in startup:
    print(line)
    time.sleep(0.1)
time.sleep(0.4)
print()

quote = random.choice(quotes)
anitext = ""
for char in quote:
    clear()
    print(Fore.RED + "\n".join(startup))
    anitext += char
    print(Fore.YELLOW + anitext + "_")
    time.sleep(0.04)

clear()
print(Fore.RED + "\n".join(startup))
print(Fore.YELLOW + anitext)

time.sleep(1)
print(Fore.RESET, end="")
print(Back.RESET)

from fs import filesystem as fs
filesystem = fs()

history = InMemoryHistory()

class bicmds:
    def whoami(self):
        print(loggedin["username"])

    def leave(self):
        print("Shutting down...")
        loggedin["fs"] = filesystem.fs
        with open("accounts/" + loggedin["username"] + ".json", "w") as towrite:
            towrite.write(json.dumps(loggedin))
        exit()

    def nothingtoseehere(self):
        print("Please type the password:")
        if prompt(">", is_password=True) == "p455w0rd":
            print("You found an easter egg!")
            print("  _")
            print(" /#\\")
            print(" \_/")
        else:
            print("NO YOU STUPID CHILD")
    
    def uninstall(self, app):
        print("Uninstalling...")
        try:
            os.remove("apps/" + app + ".py")
            filesystem.delete("apps/" + app + ".exe")
            filesystem.updateapps()
            print("done.")
        except:
            print("Error: App not found")
    
    def info(self):
        print("PyrOS")
        print("Version:", version)
        print("Username:", loggedin["username"])
        print("Host username:", os.getlogin())
        print("PyrOS process ID:", os.getpid())
    
    def cmdhelp(self):
        print("PyrOS", version)
        print("To run a file, type it's name")
        print("Commands")
        for command in commanddesc:
            try:
                cmddesc = commanddesc[command]
            except KeyError:
                cmddesc = "No description"
            print(command, "-", cmddesc)

bicmds = bicmds()

commands = {
    "cd": filesystem.cd,
    "dir": filesystem.ls,
    "ls": filesystem.ls,
    "del": filesystem.delete,
    "make": filesystem.make,
    "help": bicmds.cmdhelp,
    "notepad": filesystem.np,
    "rename": filesystem.rename,
    "read": filesystem.readprint,
    "nothingtoseehere": bicmds.nothingtoseehere,
    "whoami": bicmds.whoami,
    "move": filesystem.move,
    "clone": filesystem.clone,
    "uninstall": bicmds.uninstall,
    "info": bicmds.info,
    "exit": bicmds.leave
    }

commanddesc = {
    "cd": "Change to a different directory",
    "dir": "List items in current directory",
    "ls": "Alias of 'dir'",
    "del": "Delete a file or folder",
    "make": "Make a file or folder",
    "notepad": "Use the notepad",
    "rename": "Rename a file or folder",
    "read": "Read a file without editing it",
    "whoami": "Get your username",
    "uninstall": "Uninstall an installed app",
    "move": "Move a file",
    "clone": "Clone a file",
    "info": "Get some general info",
    "exit": "Shut down PyrOS"
    }

class appapi():
    def __init__(self):
        pass
    class accessdenied:
        pass
    def getfs(self):
        print("Access Request".center(20))
        if input("This app is requesting access to your filesystem. Give it access? [Y/N] >" + Fore.RESET).lower().startswith("y"):
            print("Access granted.")
            return filesystem
        else:
            print("Access denied.")
            return self.accessdenied
    def getbuiltins(self):
        print("Access Request".center(20))
        if input("This app is requesting access to PyrOS's builtin commands. Give it access? [Y/N] >" + Fore.RESET).lower().startswith("y"):
            print("Access granted.")
            return bicmds
        else:
            print("Access denied.")
            return self.accessdenied

def runcmd(cmd):
    cmd.strip()
    if cmd.replace(" ", "") == "":
        return
    cmd = cmd.split(" ")
    if not cmd[0] in commands:
        
        filetype = None
        
        if cmd[0].endswith(".exe"):
            filetype = "exe"
        elif cmd[0].endswith(".pkg"):
            filetype = "pkg"
        elif cmd[0].endswith(".ps"):
            filetype = "ps"
            
        if cmd[0] in filesystem.read(filesystem.cwd).keys() and filetype != None:
            try:
                clear()
                
                if filetype == "exe":
                    
                    with open("apps/" + filesystem.read(filesystem.cwd)[cmd[0]], "r") as app:
                        with open("curapp.py", "w+") as temp:
                            temp.write(app.read())
                    app = imp("curapp")
                    app.main(appapi())
                    input(Fore.YELLOW + "This application has ended, press enter to return to the terminal." + Fore.RESET)
                    
                elif filetype == "pkg":

                    with open("curapp.py", "w+") as temp:
                        temp.write(filesystem.read(filesystem.cwd)[cmd[0]])
                            
                    if input("Would you like to install this app? [Y/N]>").lower().startswith("y"):
                        print("Creating app files...")
                        with open("apps/" + cmd[0].replace(".pkg", "") + ".py", "w+") as newapp:
                            print("Installing app...")
                            with open("curapp.py", "r") as temp:
                                newapp.write(temp.read())
                                print("Updating system...")
                                filesystem.updateapps()
                                print("Successfully installed.")
                elif filetype == "ps":
                    script = filesystem.read(filesystem.cwd)[cmd[0]]
                    script = script.splitlines()
                    for item in script:
                        runcmd(item)
                
                clear()
                return
            except Exception as e:
                print(Fore.RED + "An error occurred with that app. This is usually due to broken apps, incompatible versions of software, bugs, or other stuff. Here's an error report:")
                print(str(e) + Fore.RESET)
                return
        else:
            print(Fore.RED + "Unknown app or command." + Fore.RESET)
            return
    try:
        commands[cmd[0]](*cmd[1:])
        return
            
    except TypeError as e:
        print(Fore.RED + "An error occurred, most likely you used some invalid arguments (the stuff you put after the command). Here's an error report:")
        print(str(e) + Fore.RESET)
        return
    except KeyError as e:
        print(Fore.RED + "An error occurred with that command. This is usually due to incompatible versions of software, bugs, or other stuff. Here's an error report:")
        print(str(e) + Fore.RESET)
        return

def term():
    clear()
    print(Fore.RED + 'PyrOS' + Fore.RESET, version)
    print("Type 'help' for help.")
    print("To run a file, type it's name.")
    print("Type 'exit' to shut down or your stuff won't be saved!")
    while True:
        ptext = Fore.BLUE + filesystem.cwd + ">" + Fore.RESET
        print(ptext, end="")
        cmd = input("")
        runcmd(cmd)

print("Welcome to" + Fore.RED, "PyrOS" + Fore.RESET + "!")
loggedin = None

#Logging in
while True:
    
    print()
    
    accs = [f for f in listdir("accounts")] #Getting accounts
    
    print("Accounts on this computer:" + Fore.BLUE)
    
    for acc in accs: #Printing out all accounts
        print(acc.replace(".json", ""))
        
    print()
    print(Fore.RESET + "Type 1 to login, 2 to make a new account, 3 to delete an account, or 4 to shut down.")
    print()
    option = input(">")
    print()
    
    if option == "1":
        print("Welcome! What's your username?")
        username = input(">")
        
        try:
            with open("accounts/" + username + ".json", "r") as account: #Making sure the account exists and reading it
                account = json.loads(account.read()) #Getting account info
                if account["password"] != "":
                  print("Hello,", username + "! Please type your password.")
                  while True:
                      password = prompt(">", is_password = True)
                      print("Logging in...")
                      if password == account["password"]: #Checking password
                          print("Welcome!")
                          loggedin = account #The variable for the login info
                          loggedin["username"] = username #For saving the file system
                          break
                      else:
                          print("Wrong password!")
                          break
                else:
                  loggedin = account #The variable for the login info
                  loggedin["username"] = username #For saving the file system
                  print("Welcome!")
        except:
            print("That's not an account!") #If the account doesn't exist
            
    elif option == "2":
        
        print("What do you want your username to be?")
        username = input(">")
        print("And your password? (leave blank for no password)")
        password = input(">")
        print("Making your account...")
        
        cont = True
        print("Checking for existing account...")
        
        if isfile("accounts/" + username + ".json"):
            print("That account already exists.")
            cont = False
            
        if cont:
            with open("accounts/" + username + ".json", "w+") as account:
                
                newacc = {"password": password, "fs":{ 
            "apps": {},
            "readme.txt": """
Welcome to PyrOS!
* Use the 'help' command for a list of commands
* Type the name of a file to execute it if it's an executable (.exe, .pkg, .ps)
* Use the 'notepad' command to edit files
* Users have their own files, but every user has access to all of the apps on this computer

WARNING: Installing apps from unknown sources could be dangerous! Although PyrOS asks you before letting any apps access the PyrOS file system, we can't say the same for your actual file system. Make sure an app is safe before running it!
""",
            "PyrOS": {
                "system.exe": "[PyrOS_DO_NOT_DELETE]642b3708b7c809ynv0f8y084yrcnc78cnyd747x74yxuew8fb7n5y8syb7nyd78nystxd7yn7tyn3c97vnvyymf0r7eyntcynvner70tcytvcncgeycny74cyn45nyrvgn7ygnnycgnudye8yruhudhfuufdhfudhugfd4578548",
                
                "helloworld.pkg": """def main(api):
    print("Hello world!")"""}}}
                
                account.write(json.dumps(newacc))
                print("New account created!")
                
    elif option == "3":
        print("Which account do you want to delete?")
        acc = input(">")
        print("Deleting...")
        
        try:
            os.remove("accounts/" + acc + ".json")
            print("Deleted.")
        except:
            print("Account not found.")
    
    elif option == "4":
        sys.exit()
        
    else:
        print("Invalid option.")
    
    if loggedin != None:
        break

time.sleep(0.3)
filesystem.fs = loggedin["fs"]
filesystem.updateapps()

term()
