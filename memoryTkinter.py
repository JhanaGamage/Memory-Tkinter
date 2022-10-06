from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk # Librairie de traitement d'image
import os # Provides functions for creating and removing a directory (folder), fetching its contents
import random # Defines a series of functions for generating or manipulating random integers
import customtkinter

workingdir = os.getcwd()
my_library = "Fruits"
cards_list = []
count = 0
selected_cards = []
trials_number = 0
found_pairs = 0

# Interface
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("dark-blue") 
root = customtkinter.CTk()
root.title("Jeu de mémoire")
root.geometry("800x800")

class Memory_Card(Button):
    PRIME=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    
    def __init__(self, parent, num) -> None:
        Button.__init__(self, parent, text = '')
        self.parent = parent
        self.numero = num # Correspond au numéro de la carte
        self.valeur = self.PRIME[num // 2] # Division entière
        self.img_back= ''
        self.img_front = ''
        self.configure(command = self.handle)

    def handle(self):
        global count, selected_cards, cards_list, trials_number, found_pairs, info
        if count < 2:
            selected_cards.append(self)
            count += 1
            self["image"] = self.img_front
        # Si 2 cartes sont sélectionnées 
        if len(selected_cards) == 2:
            print("Deux cartes selectionnées", selected_cards[0].numero, selected_cards[1].numero)
            
            if selected_cards[0].valeur%selected_cards[1].valeur == 0 and selected_cards[0].numero != selected_cards[1].numero:
                messagebox.showinfo("Succès", "Succès")
                print("succès")
                for i in selected_cards:
                    i.configure(state = "disable")
                count = 0
                selected_cards = []
                found_pairs += 1
            else:
                # Cacher les cartes après une seconde
                self.parent.after(200, self.hide_card)
        
        # Incrémente nombre de tentatives
        trials_number += 1
        #info["text"] = str(trials_number // 2)

    def set_img_front(self, img):
        self.img_front = img

    def set_img_back(self, img):
        self.img_back = img
        self['image'] = self.img_back   
    
    def hide_card(self):
        #print("hide_card()")
        global selected_cards, count
        #print(f'[hide_cards: {selected_cards}')
        # Vérifier que toutes les paires sont trouvées
        if(found_pairs == len(cards_list) // 2):
            messagebox.showinfo("Fin de la partie ! /n", str(found_pairs) + " paires trouvées en " + str(trials_number // 2) + " tentatives")
        for i in selected_cards:
        #   i["stage"] = NORMAL
            i["image"] = self.img_back
        count = 0
        selected_cards = []

list_img = []
def getImgDir(folder): #La fonction est copiée collée juste en dessous
    global list_img
    list_img = []
    for i in os.listdir(os.path.join(os.getcwd(), folder)):
        if i.endswith(".png"):
            list_img.append(i) # Ajoute au tableau qui contient la liste du nom des images

getImgDir("Fruits")


def reset_handle():
    global cards_list, my_frame, trials_number, count, selected_cards, found_pairs, Level
    count = 0
    selected_cards = []
    trials_number = 0
    found_pairs = 0
    random.shuffle(cards_list)
    # Repositionne les cartes sur le tapis
    for i in range(0, lig):
        for j in range(0, col):
            cards_list[i*col+j].grid(row = i, column = j)
    for i in cards_list:
        i["image"] = img_bb
        i["state"] = NORMAL
    my_frame.update()

col = 5
lvl = 2
def setGrid(lvl = None):
    print("Set grid ", lvl)
    global lig
    if lvl == 1:
        lig = 2
    #    root.geometry("480x240")
    elif lvl == 2:
        lig = 4
    #    root.geometry("480x400")
    elif lvl == 3:
        lig = 6
    #    root.geometry("480x580")
    elif lvl == None:
        lig = 2
    #    root.geometry("480x240")
    reset_handle


setGrid()

my_frame = Frame(root) # conteneur
my_frame.pack(pady = 45, padx = 45)

# Définition de l'arrière des cartes
img_back = Image.open(os.getcwd() + '/' + 'img_lib_fruits.png')
img_back = img_back.resize((64, 64))
img_bb = ImageTk.PhotoImage(img_back)

# Création du jeu de cartes
def generateCardCarpet():
    global lig
    print("generate card carpet ", lig)
    img_index = 0
    for i in range(0, col * lig):
        B = Memory_Card(my_frame, i)
        B.set_img_back(img_bb)
        # B.set_img_back(ImageTk.PhotoImage(img_back))
        if img_index > (len(list_img) - 1): 
            img_index = 0

        ## Nombre impair
        if i%2 == 0:
           # img = Image.open(list_img[i])
            img = Image.open(os.getcwd() + '/Fruits/' + list_img[img_index])
            img = img.resize((64,64))
           # img = img.filter(ImageFilter.Color3DLUT((10,10,10), [[30,30,30,30]] * 27, channels=4))
            B.set_img_front(ImageTk.PhotoImage(img))
        else:
            B.set_img_front(ImageTk.PhotoImage(img))
        cards_list.append(B)
        img_index += 1

    random.shuffle(cards_list)

    # Positionne les cartes sur le tapis
    for i in range(0, lig):
        for j in range(0, col):
            cards_list[i*col+j].grid(row = i, column = j)

generateCardCarpet()

txt_info = Label(root, text = "Nombres de tentatives: " + str(trials_number))
txt_info.pack(side = LEFT, padx = 20, pady = 20)

isModeWindowOpen = 0
def mode_select():
    #global isModeWindowOpen
    #if isModeWindowOpen: return
    #else:
    #    isModeWindowOpen = 1
    Mode_Window(root)

reset = customtkinter.CTkButton(root, text = "RESET", command = reset_handle)
reset.pack(side = RIGHT, padx = 10, pady = 10)
mode = customtkinter.CTkButton(root, text="MODE", command = mode_select)
mode.pack(side = RIGHT, padx = 10, pady = 10)

# Fenêtre de choix du mode de jeu et de la difficulté
class Mode_Window(Toplevel): # TopLevel = fenêtre primaire indépendante
    M = [1,2,3]
    Levels = ["Niveau 1", "Niveau 2", "Niveau 3"]
    lib = ["Fruits", "Animaux", "Cartoons"]

    def __init__(self, parent):
        global lvl, my_library
        super().__init__(parent)
        self.parent = parent
        self.title("Sélection du mode")
        self.geometry("200x700")
        self.okButton = Button(self, text = "OK", command = self.valid)
        self.okButton.pack(side = BOTTOM)
        self.frameLevel = Frame(self)
        self.frameLevel.pack(pady = 20)
        self.libraryFrame = Frame(self)
        self.libraryFrame.pack(pady = 20)
        
        self.sel = IntVar()
        print(lvl)
        self.sel.set(lvl)
        for i in range(0, len(self.Levels)):
            self.selMode = Radiobutton(self.frameLevel, variable = self.sel, text = self.Levels[i], value = self.M[i])
            self.selMode.pack(padx = 30, pady = 30)

        self.selLib = StringVar()
        self.selLib.set(my_library)
        for i in range(0, len(self.lib)):
            self.selRep = Radiobutton(self.libraryFrame, variable = self.selLib, text = self.lib[i], value = self.lib[i])
            self.selRep.pack(padx=30, pady=30)
            self.grab_set()

    def valid(self):
        global lvl, cards_list, my_frame, lig, col, list_img, trials_number, found_pairs
        newLvl = self.sel.get()
        folder = self.selLib.get()

        print("new level = ", newLvl)
        setGrid(newLvl) # Nombre de colonnes et de lignes
        # Charger images répertoire
        getImgDir(folder)

        cards_list = []
        generateCardCarpet()
        lvl = newLvl
        my_frame.update()
        self.destroy()

root.mainloop()