import bs4
import math
import requests
import tkinter as tk
from tkinter import ttk

class dofus_frame(tk.Tk):
"""
this is the main frame. It store all the pages
"""
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
    """
    this function show you the page in argument
    """
        frame = self.frames[framekey]
        frame.tkraise()

    def get_page(self, classname):
    """
    Take the name f the page and return the objet page
    """
        return self.frames[classname]


class StartPage(tk.Frame):
"""
Page with the different choice.
Use to select which objetct you want to craft and its characteristics
"""
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
        self.listbonussec = tk.Listbox(self, selectmode='multiple', exportselection=0)
        for i, j in sorted(bonus_secondaire.items()):
            self.listbonussec.insert(j, i)
        self.And_or_prim = tk.StringVar()
        self.And_or_seco = tk.StringVar()
        Button1 = tk.Radiobutton(self, text="And", variable=self.And_or_prim, value="AND")
        Button2 = tk.Radiobutton(self, text="Or", variable=self.And_or_prim, value="OR")
        Button1.select()
        Button3 = tk.Radiobutton(self, text="And", variable=self.And_or_seco, value="AND")
        Button4 = tk.Radiobutton(self, text="Or", variable=self.And_or_seco, value="OR")
        Button3.select()
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
        Button1.grid(row=5, column=0)
        Button2.grid(row=5, column=1)
        self.listbonussec.grid(row=3, column=2, columnspan=2, rowspan=2)
        Button3.grid(row=5, column=2)
        Button4.grid(row=5, column=3)
        text_levelmin.grid(row=6, column=1)
        text_levelmax.grid(row=7, column=1)
        tk.Label(self, text="Level min").grid(row=6, column=0)
        tk.Label(self, text="Level max").grid(row=7, column=0)
        Launchsearch.grid(row=6, column=2, rowspan=2)


class PageOne(tk.Frame):
    """
    This page gave you the result with a list of item. 
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 1")
        label.grid(row=0, column=0, columnspan=1)
        button = ttk.Button(self, text="Back to home", command=self.update)
        button.grid(row=2, column=0, columnspan=1)

    def update(self):
        """
        Update will do the request and return  you the list of item in a list in the GUI in witch you can choose witch items you need
        """
        start_page = self.controller.get_page(StartPage)
        value_list_item = start_page.listitem.curselection()
        value_list_arme = start_page.listarme.curselection()
        value_list_bonus = start_page.listbonus.curselection()
        value_list_bonus_sec = start_page.listbonussec.curselection()
        list_link_item = []
        if value_list_item is not None:
            s = "http://www.dofus.com/fr/mmorpg/encyclopedie/equipements?text="
            for i in value_list_item:
                s = s + "&type_id[]=" + str(list_object[start_page.listitem.get(i)])
            if value_list_bonus is not None:
                for i in value_list_bonus:
                    s = s + "&EFFECTMAIN[]=" + str(
                        bonus_primaire[start_page.listbonus.get(i)])
                s = s + "&EFFECTMAIN_and_or=" + str(start_page.And_or_prim.get())
            if value_list_bonus_sec is not None:
                for i in value_list_bonus_sec:
                    s = s + "&EFFECT[]=" + str(
                        bonus_primaire[start_page.listbonus.get(i)])
                s = s + "&EFFECT_and_or=" + str(start_page.And_or_prim.get())
            s = s + "&size=96"
            print(s)
            site = requests.get(s)
            # f = open('test.txt', 'w')
            soup = bs4.BeautifulSoup(site.text, 'html.parser')
            number_result = 1
            if(soup.find("div", class_="ak-list-info") is not None):
                number_result = soup.find("div", class_="ak-list-info").strong.string
            number_page = math.ceil(int(number_result) / 96)
            for link in soup.tbody.find_all('a'):
                list_link_item.append(link.get('href'))
            for i in range(2, number_page + 1):
                w = s + "&page=" + str(i)
                print(w)
                site = requests.get(w)
                soup = bs4.BeautifulSoup(site.text, 'html.parser')
                for link in soup.tbody.find_all('a'):
                    list_link_item.append(link.get('href'))
            list_link_item = list(set(list_link_item))
            self.list_name_item = {}
            self.resultlist = tk.Listbox(self, selectmode='multiple', exportselection=0)
            for link in list_link_item:
                site = requests.get("http://www.dofus.com" + link)
                soup = bs4.BeautifulSoup(site.text, 'html.parser')
                craft_panel = soup.find("div", class_="ak-container ak-panel ak-crafts")
                if craft_panel is not None:
                    dic_name_nb = {}
                    for ressources in craft_panel.find_all("div", class_="ak-list-element"):
                        nbressource = ressources.find("div", class_="ak-front").text
                        nameressource = ressources.find(
                            "div", class_="ak-content").find("span", class_="ak-linker").text
                        dic_name_nb[nameressource] = int(nbressource[:-4])
                    self.list_name_item[soup.find(
                        "h1", class_="ak-return-link").text.replace(' ', '').replace('\n', '')] = dic_name_nb
                else:
                    list_link_item.remove(link)
            for i, j in enumerate(self.list_name_item):
                self.resultlist.insert(i, j)
            self.resultlist.selection_set(0, self.resultlist.size() - 1)
            self.resultlist.grid(row=1, column=0)
            button = ttk.Button(self, text="Print to file", command=self.printresultfile)
            button.grid(row=2, column=1, columnspan=1)

    def printresultfile(self):
        """
        print all the item needed to craft the items selected a file name "listressource.txt"
        """
        itemvoulu = self.resultlist.curselection()
        list_ressource = {}
        for i in itemvoulu:
            print(i)
            print(self.list_name_item)
            for item, value in self.list_name_item[self.resultlist.get(i)].items():
                if item in list_ressource:
                    list_ressource[item] = list_ressource[item] + value
                else:
                    list_ressource[item] = value
        f = open("listressource.txt", "w")
        for item in list_ressource:
            print(item + ": " + str(list_ressource[item]), file=f)
        f.close()


list_object = {"ammulette": 1, "anneau": 9, "bottes":  11, "bouclier": 82,
               "cape": 17, "ceinture": 10, "chapeau": 16,
               "sac a dos": 81, "trophee": 151}
list_armes = {"arc": 2, "baguette": 3,
              "baton": 4, "dague": 5, "faux": 22,
              "hache": 19, "marteau": 7, "pelle": 8, "epee": 6}


bonus_primaire = {"Agilité": 8, "Chance": 9, "Critique": 10, "Force": 4,
                  "Intelligence": 7, "Invocations": 23, "Pa": 2, "Pm": 3, "Po": 11}
bonus_secondaire = {"Sagesse": 6, "Soins": 113, "Tacle": 344, "Vitalité": 5}
And_Or_seco = "AND"

if __name__ == "__main__":
    app = dofus_frame()
    app.mainloop()

