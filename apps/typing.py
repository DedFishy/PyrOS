def main(api):
    from os import system as hostcmd
    from os import name as hostname
    from time import sleep

    def clear():
        if hostname == "nt":
            hostcmd("cls")
        else:
            hostcmd("clear")

    text = input("Enter some text >")

    anitext = ""

    clear()


    for char in text:
        anitext += char
        print(anitext + "_")
        sleep(0.3)
        clear()

