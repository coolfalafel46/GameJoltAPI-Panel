import sys
sys.path.insert(1, './Modules')
import ast
import py_gjapi
import tkinter
import customtkinter  # <- import the CustomTkinter module
import requests
from PIL import Image
import os

from py_gjapi import GameJoltTrophy

root_tk = customtkinter.CTk()  # create the Tk window like you normally do
root_tk.geometry("480x650")
root_tk.title("GameJoltAPI Panel")
customtkinter.set_default_color_theme("green")

my_font = customtkinter.CTkFont(family="Arial", size=18, weight="bold")

logo = customtkinter.CTkImage(light_image=Image.open(r"./Game_Jolt_Logo.png"), dark_image=Image.open(r"./Game_Jolt_Logo.png"), size=(250, 27.5))

logo_label = customtkinter.CTkLabel(root_tk, image=logo, text="")

logo_label.grid(row = 0, column = 0, padx = 120, pady = 30)

uEContent = customtkinter.StringVar()
tEContent = customtkinter.StringVar()
gIDContent = customtkinter.StringVar()
pKContent = customtkinter.StringVar()

def button_event():
    GetEntries = [
            usernameEntry.get(),
            tokenEntry.get(),
            gameIDEntry.get(),
            privateKeyEntry.get()
    ]

    loginCache(GetEntries)

    GameJoltTrophy(GetEntries[0], GetEntries[1], GetEntries[2], GetEntries[3])

    print(GetEntries)

    #destroy 
    if GetEntries[0] != "" and GetEntries[1] != "" and GetEntries[2] != "" and GetEntries[3] != "":
        usernameEntry.destroy()
        tokenEntry.destroy()
        gameIDEntry.destroy()
        privateKeyEntry.destroy()
        buttonCheck.destroy()
        #logo_label.destroy()
        mainPanel(GetEntries)

def loginCache(GetEntries):
    if not os.path.exists("./ApiCache/Login.txt"):
        os.mkdir("./ApiCache")
        entriesFile = open("./ApiCache/Login.txt", "w")
        entriesFile.write(str(GetEntries))
        entriesFile.close()
    else:
        entriesFile = open("./ApiCache/Login.txt", "r")
        GetEntries = ast.literal_eval(entriesFile.read())  # преобразование строки в список
        uEContent.set(value=GetEntries[0])
        tEContent.set(value=GetEntries[1])
        gIDContent.set(value=GetEntries[2])
        pKContent.set(value=GetEntries[3])

        entriesFile.close() 


usernameEntry = customtkinter.CTkEntry(root_tk, textvariable=uEContent, placeholder_text="Username", width = 200, height = 20)
buttonCheck = customtkinter.CTkButton(root_tk, text="✅", command=button_event, width=20)
buttonCheck.grid(row = 6, column = 0, pady = 0)

usernameEntry.grid(row = 1, column = 0)

tokenEntry = customtkinter.CTkEntry(root_tk, textvariable=tEContent,placeholder_text="Token", width = 200, height = 20)
tokenEntry.grid(row = 3, pady = 10)

gameIDEntry = customtkinter.CTkEntry(root_tk, textvariable=gIDContent,placeholder_text="Game ID", width = 200, height = 20)
gameIDEntry.grid(row = 4, pady = 0)

privateKeyEntry = customtkinter.CTkEntry(root_tk, textvariable=pKContent,placeholder_text="Private Key", width = 200, height = 20)
privateKeyEntry.grid(row = 5, pady = 10)

    




def mainPanel(GetEntries):
    gjt=GameJoltTrophy(GetEntries[0], GetEntries[1], GetEntries[2], GetEntries[3])
    
    if not os.path.exists("./ApiCache/" + GetEntries[0] + "'s pfp.jpg"):
        pfp = requests.get(gjt.fetchUserInfo()["users"][0]["avatar_url"],stream=True)
        pfpFile = open("./ApiCache/"+GetEntries[0]+"'s pfp.jpg", "wb")
        pfpFile.write(pfp.content)
        pfpFile.close()
    pfpFile=open("./ApiCache/"+GetEntries[0]+"'s pfp.jpg","rb")

    userIcon = customtkinter.CTkImage(
                                        light_image=Image.open(pfpFile),
                                        dark_image=Image.open(pfpFile),
                                        size=(64,64)
                                    )
    
    icon_label = customtkinter.CTkLabel(root_tk, image=userIcon, text="")

    

    tableIDEntry = customtkinter.CTkEntry(root_tk, placeholder_text="Table ID", width=60, height=20)
    tableIDEntry.grid(row = 8, column = 0)

    icon_label.grid(row = 1,)

    usernameLabel = customtkinter.CTkLabel(root_tk, text=GetEntries[0], width=100, height=20)
    usernameLabel.grid(row = 2)

    trophyLabel = customtkinter.CTkLabel(root_tk, font=my_font, text="Trophies", width=100, height=20)
    trophyLabel.grid(row = 3, pady=10)

    scoresLabel = customtkinter.CTkLabel(root_tk, font=my_font, text="Scores", width=100, height=20)
    scoresLabel.grid(row = 6,pady=10)
    
    trophyEntry = customtkinter.CTkEntry(root_tk, placeholder_text="Trophy ID", width=100, height=20)
    trophyEntry.grid(row = 4)

    sortEntry = customtkinter.CTkEntry(root_tk, placeholder_text="Sort", width=40, height=20)
    sortEntry.grid(row = 7, column = 0)

    scoreEntry = customtkinter.CTkEntry(root_tk, placeholder_text="Score", width=50, height=20)
    scoreEntry.grid(row = 9, column = 0)

    scoreNameEntry = customtkinter.CTkEntry(root_tk, placeholder_text="Name (Example:Score + Name)", width=190)
    scoreNameEntry.grid(row = 10)

    def addTrophy():
        gjt.addAchieved(int(trophyEntry.get()))
        trophyEntry.select_clear()

    def addScore():
        gjt.addScores(scoreEntry.get() + " " + scoreNameEntry.get(),int(sortEntry.get()), tableIDEntry.get())

    buttonCheckTrophy = customtkinter.CTkButton(root_tk, text="Add Trophy", command=addTrophy,width=20)
    buttonCheckTrophy.grid(row = 5, pady = 10)

    buttonCheckScore = customtkinter.CTkButton(root_tk, text="Add Scores", command=addScore,width=20)
    buttonCheckScore.grid(row = 11, pady = 10)



root_tk.mainloop()

