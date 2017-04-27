import urllib
import json
import numpy as np
import pandas as pd
import bs4
import math
import sys
import time
import argparse
import requests
from PIL import Image
from requests.adapters import HTTPAdapter
import tkinter as tk
from tkinter import ttk

# parser = argparse.ArgumentParser()
# parser.add_argument("item", type=str, nargs='+',
#                     help="display a square of a given number")
# parser.add_argument("-m", "--levelmin", type=int,
#                     help="set the min level")
# parser.add_argument("-M", "--levelmax", type=int,
#                     help="set the max level")
# parser.add_argument("-c", "--charach", type=)
# args = parser.parse_args()


def RetrieveData(search_item):
    if search_item != None:
        print(search_item)


class dofus_frame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        mainframe = tk.Frame(self)
        mainframe.pack(side="top", fill="both", expand=True)

        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for f in (StartPage, PageOne):
            frame = f(parent=mainframe, controller=self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, framekey):
        frame = self.frames[framekey]
        frame.tkraise()

    def get_page(self, classname):
        # for page in self.frames.values():
        #     if str(page.__class__.__name__) == classname:
        #         return self.frames[page]
        return self.frames[classname]


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.listitem = tk.Listbox(self, selectmode='multiple', width=20,
                                   height=10, exportselection=0)
        for i, j in sorted(list_object.items()):
            self.listitem.insert(j, i)
        self.listarme = tk.Listbox(self, selectmode='multiple', width=20,
                                   height=10, exportselection=0)
        for i, j in sorted(list_armes.items()):
            self.listarme.insert(j, i)
        self.listbonus = tk.Listbox(self, selectmode='multiple', exportselection=0)
        for i, j in sorted(bonus_primaire.items()):
            self.listbonus.insert(j, i)
        self.And_or_prim = tk.StringVar()
        Button1 = tk.Radiobutton(self, text="And", variable=self.And_or_prim, value="AND")
        Button2 = tk.Radiobutton(self, text="Or", variable=self.And_or_prim, value="OR")
        Button1.select()
        self.levelmin = tk.IntVar()
        self.levelmin.set(1)
        text_levelmin = tk.Entry(self, textvariable=self.levelmin, width=4)
        self.levelmax = tk.IntVar()
        self.levelmax.set(200)
        text_levelmax = tk.Entry(self, textvariable=self.levelmax, width=4)
        Launchsearch = ttk.Button(self, text="Go",
                                  command=lambda: controller.show_frame(PageOne))

        tk.Label(self, text="Liste Items").grid(row=0, column=0, columnspan=2)
        tk.Label(self, text="Liste Armes").grid(row=0, column=2)
        self.listarme.grid(row=1, column=2)
        self.listitem.grid(row=1, column=0, columnspan=2)
        tk.Label(self, text="Bonus").grid(row=2, column=0, columnspan=3)
        self.listbonus.grid(row=3, column=0, columnspan=2, rowspan=2)
        Button1.grid(row=3, column=2)
        Button2.grid(row=4, column=2)
        text_levelmin.grid(row=5, column=1)
        text_levelmax.grid(row=6, column=1)
        tk.Label(self, text="Level min").grid(row=5, column=0)
        tk.Label(self, text="Level max").grid(row=6, column=0)
        Launchsearch.grid(row=5, column=2, rowspan=2)

    def test(self):
        print(self.levelmax.get())


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 1")
        label.grid(row=0, column=0, columnspan=1)
        button = ttk.Button(self, text="Back to home", command=self.update)
        button.grid(row=2, column=0, columnspan=1)

    def update(self):
        start_page = self.controller.get_page(StartPage)
        value_list_item = start_page.listitem.curselection()
        value_list_arme = start_page.listarme.curselection()
        value_list_bonus = start_page.listbonus.curselection()
        if value_list_item != None:
            s = "http://www.dofus.com/fr/mmorpg/encyclopedie/equipements?text="
            for i in value_list_item:
                s = s + "&type_id[]=" + str(list_object[start_page.listitem.get(i)])
            if value_list_bonus != None:
                for i in value_list_bonus:
                    s = s + "&EFFECTMAIN[]=" + str(
                        bonus_primaire[start_page.listbonus.get(i)])
                s = s + "&EFFECT_and_or=" + str(start_page.And_or_prim.get())
            print(s)
        # RetrieveData(StartPage.listarme.curselection())
        # test = tk.Listbox(self, selectmode='multiple', exportselection=0)
        # test.grid(row=1, column=0, columnspan=1)


list_object = {"ammulette": 1, "anneau": 9, "bottes":  11, "bouclier": 82,
               "cape": 17, "ceinture": 10, "chapeau": 16,
               "sac a dos": 81, "trophee": 151}
list_armes = {"arc": 2, "baguette": 3,
              "baton": 4, "dague": 5, "faux": 22,
              "hache": 19, "marteau": 7, "pelle": 8, "epee": 6}


bonus_primaire = {"Agilité": 8, "Chance": 9, "Critique": 10, "Force": 4,
                  "Intelligence": 7, "Invocations": 23, "Pa": 2, "Pm": 3, "Po": 11}


class test(object):
    def __init__(self, root, **kwargs):
        self.frame = root
        self.frame.minsize(860, 265)
        k = 0
        for i, j in list_object.items():
            button = Checkbutton(root, text=i, variable=j)
            button.pack()


if __name__ == "__main__":
    app = dofus_frame()
    app.mainloop()

# bonus_secondaire = {"% Critique sur le sort": , "% Dommages aux sorts": , "% Dommages d'armes": , "% Dommages distance": , "% Dommages mêlée": , "% Résistance Air": , "% Résistance Eau": , "% Résistance Feu": , "% Résistance Neutre": , "% Résistance Terre": , "% Résistance distance": , "% Résistance mêlée": , "- % Résistance Eau": , "- % Résistance Neutre": , "- Agilité": , "- Chance": , "- Dommages Air": , "- Dommages Critiques": , "- Dommages Eau": , "- Dommages Feu": , "- Dommages Neutre": , "- Dommages Poussée": , "- Dommages Terre": , "- Esquive PA": , "- Esquive PM": , "- Force": , "- Fuite": , "- Initiative": , "- Intelligence": , "- PA": , "- PM": , "- Portée": , "- Prospection": , "- Retrait PA": , "- Retrait PM": , "- Résistance Critiques": , "- Résistance Poussée": , "- Sagesse": , "- Tacle": , "- Vitalité": , "-% Critique": , "-% Dommages aux sorts": , "-% Dommages d'armes": , "-% Dommages distance": , "-% Dommages mêlée": , "-% Résistance Air": , "-% Résistance Feu": , "-% Résistance Terre": , "-% Résistance distance": , "-% Résistance mêlée": , "Attitude": , "Dommages": , "Dommages Air": , "Dommages Critiques": , "Dommages Eau": , "Dommages Feu": , "Dommages Neutre": , "Dommages Pièges": , "Dommages Poussée": , "Dommages Terre": , "Dommages sur le sort": , "Esquive PA": , "Esquive PM": , "Fuite": , "Initiative": , "Pods": , "Prospection": , "Puissance": , "Puissance (pièges)": , "Renvoie dommages": , "Retrait PA": , "Retrait PM": , "Résistance Air": , "Résistance Critiques": , "Résistance Eau": , "Résistance Feu": , "Résistance Neutre": , "Résistance Poussée": , "Résistance Terre": , "Sagesse": , "Soins": , "Tacle": , "Vitalité": }
# And_Or_seco = "AND"
# element = []

# s = "http://www.dofus.com/fr/mmorpg/encyclopedie/equipements?text="
# for i in args.item:
#     s = s + "&type_id[]=" + str(list_object[i])
# if args.levelmin:
#     s = s + "&object_level_min=" + str(args.levelmin)
# if args.levelmax:
#     s = s + "&object_level_max=" + str(args.levelmax)
# if args.
# print(s)
# site = requests.get(s)
# print(site)

#
# s = requests.Session()
# s.mount('https://www.dofus.fr', HTTPAdapter(max_retries=5))
# s.headers["User-Agent"] = "PlacePlacer"
# r = s.post("https://www.reddit.com/api/login/{}".format(username),
#            data={"user": username, "passwd": password, "api_type": "json"})
# s.headers['x-modhash'] = r.json()["json"]["data"]["modhash"]
