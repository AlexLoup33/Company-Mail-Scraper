__author__ = "Lou-Poueyou Alexandre | github.com/AlexLoup33"

import tkinter as tk

from customtkinter import *
from tkinter import messagebox, filedialog as fd
from pathlib import Path

from modules.scrapper import scrapRevenue, scrapActivity, scrapFromFile, csvPath
from modules.globalVar import departementLinks, ActivityLinks

light_gray = "#FAFAFA"
green = "#AEEEE0"

logoPath = Path(__file__).parent.joinpath("res")
applogoPath = Path(__file__).parent.joinpath("res/applogo.png") #Scraping icons created by orvipixel - Flaticon - https://www.flaticon.com/free-icons/scraping

departementLinksKey = list(departementLinks.keys())
ActivityLinksKey = list(ActivityLinks.keys())

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, textColor, bg, radius=25, padding=10, command=None, width=150, height=50, **kwargs):
        super().__init__(parent, width=width, height=height,bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.radius = radius
        self.padding = padding

        # Dessiner le rectangle arrondi
        self.button = round_canvas(self, padding, padding, 
                                   width-padding, 
                                   height-padding, 
                                   radius=self.radius, 
                                   fill=light_gray, 
                                   outline=green,
                                   width=2)

        # Créer le texte
        self.text = self.create_text(width/2, height/2, 
                                     text=text, 
                                     font=("CenturyGothic", 18),
                                     justify="center", 
                                     fill=textColor, 
                                     width=width-4*padding)  # Adjust width for text wrapping

        # Lier l'événement de clic
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.animationSteps = 10

    def on_click(self, event):
        if self.command:
            self.command()
    
    def on_enter(self, event):
        # Changer la couleur du bouton
        self.animate_color(light_gray, green)

    def on_leave(self, event):
        self.animate_color(green, light_gray)

    def animate_color(self, startColor, endColor):
        startColorRgb = self.winfo_rgb(startColor)
        endColorRgb = self.winfo_rgb(endColor)

        r_diff = (endColorRgb[0] - startColorRgb[0]) / self.animationSteps
        g_diff = (endColorRgb[1] - startColorRgb[1]) / self.animationSteps
        b_diff = (endColorRgb[2] - startColorRgb[2]) / self.animationSteps

        self.animationStep = 0

        def perform_animation():
            if self.animationStep <= self.animationSteps:
                newColor = (
                    int(startColorRgb[0] + r_diff * self.animationStep),
                    int(startColorRgb[1] + g_diff * self.animationStep),
                    int(startColorRgb[2] + b_diff * self.animationStep)
                )
                hexColor = f'#{newColor[0]//256:02x}{newColor[1]//256:02x}{newColor[2]//256:02x}'
                self.itemconfig(self.button, fill=hexColor)
                self.animationStep += 1
                self.after(20, perform_animation)

        perform_animation()

def round_canvas(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def on_button_click():
    print("Button clicked")


def App():
    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(False, False)
    root.title("Scrapp.io")
    
    icon = tk.PhotoImage(file=applogoPath)
    root.wm_iconphoto(False, icon)

    options_frame = tk.Frame(root, bg=light_gray)

    lpath = logoPath.joinpath("logo.png")
    img = tk.PhotoImage(file=lpath)
    logo = tk.Label(options_frame, image=img, bg=light_gray)
    logo.place(x = 10, y = 20)

    canvasCA = tk.Canvas(options_frame, width=250, height=100, bg=light_gray, highlightthickness=0)
    canvasCA.place(x = 20, y = 150)
    topRevenueButton = RoundedButton(canvasCA, text=f"Recherche par Revenue", textColor="black", bg=green, command=lambda: showPage(TopRevenuePage), padding=10, width=250, height=100)
    topRevenueButton.pack()

    canvasActivity = tk.Canvas(options_frame, width=250, height=100, bg=light_gray, highlightthickness=0)
    canvasActivity.place(x = 20, y = 350)
    activityButton = RoundedButton(canvasActivity, text="Recherche par Activité", textColor="black", bg=green, command=lambda: showPage(ActivityPage), padding=10, width=250, height=100)
    activityButton.pack()

    canvasFile = tk.Canvas(options_frame, width=250, height=100, bg=light_gray, highlightthickness=0)
    canvasFile.place(x = 20, y = 550)
    fileButton = RoundedButton(canvasFile, text="Recherche à partir d'un fichier existant", textColor="black", bg=green, command=lambda: showPage(FilePage), padding=10, width=250, height=100)
    fileButton.pack()

    options_frame.pack(side=tk.LEFT)
    options_frame.pack_propagate(False)
    options_frame.configure(width=280, height=720)

    main_frame = tk.Frame(root, bg="white", highlightbackground=light_gray, highlightthickness=2)
    main_frame.pack(side=tk.LEFT)
    main_frame.pack_propagate(False)
    main_frame.configure(width=1000, height=720)

    def showPage(page):
        deletePage()
        page()

    def deletePage():
        for frame in main_frame.winfo_children():
            frame.destroy()

    def TopRevenuePage():
        topRevenueFrame = tk.Frame(main_frame, background="white")

        canvasTitle = tk.Canvas(topRevenueFrame, width=250, height=100, bg="white", highlightthickness=0)
        title = tk.Label(canvasTitle, text="Recherche à partir des revenues", font=("CenturyGothic", 24), fg="black", bg="white")

        #Create an transparant separator between the title and the option menu
        separatorTitle = tk.Frame(topRevenueFrame, height=40, width=450, bg="white")

        departement = tk.StringVar()
        departement.set("Ain - 01")

        departementMenu = CTkOptionMenu(topRevenueFrame, width=450, height= 50, fg_color=green, button_color=green, button_hover_color=green,
                                        text_color="black", corner_radius=10, values=departementLinksKey, variable=departement)
        
        separatorOptionM = tk.Frame(topRevenueFrame, height=40, width=450, bg="white")

        numberEntry = CTkEntry(topRevenueFrame, width=450, height=50, border_color="white", fg_color=green,
                               text_color="black", corner_radius=10, placeholder_text="Nombre d'entreprise à scraper") 
        
        separatorNumber = tk.Frame(topRevenueFrame, height=40, width=450, bg="white")

        csvFileName = CTkEntry(topRevenueFrame, width=450, height=50, border_color="white", fg_color=green, 
                               text_color="black", corner_radius=10, placeholder_text="Nom du fichier csv")

        separatorCSV = tk.Frame(topRevenueFrame, height=40, width=450, bg="white")

        tabName = CTkEntry(topRevenueFrame, width=450, height=50, border_color="white", fg_color=green, 
                           text_color="black", corner_radius=10, placeholder_text="Nom du tableur")

        separatorTab = tk.Frame(topRevenueFrame, height=40, width=450, bg="white")

        fileName = CTkEntry(topRevenueFrame, width=450, height=50, border_color="white", fg_color=green,
                                 text_color="black", corner_radius=10, placeholder_text="Nom du fichier tableur")

        separatorFileName = tk.Frame(topRevenueFrame, height=40, width=450, bg="white")

        switchMail = tk.BooleanVar()
        switchMail.set(False)
        switchMailButton = CTkSwitch(topRevenueFrame, text="Recherches des mails ?", text_color="black", width=450, height=50, 
                                    fg_color="red", bg_color="white", button_color="#DCDCDC", button_hover_color="#DCDCDC", variable=switchMail, corner_radius=10)

        def button_command():
            try:
                number = int(float(numberEntry.get()))
            except ValueError:
                messagebox.showerror("Error", "Le nombre de sociétés doit être un nombre") # type = ignore
                return
            return scrapRevenue(departementLinks[departement.get()], number, csvFileName.get(), tabName.get(), fileName.get(), switchMail.get())

        scrapButton = CTkButton(topRevenueFrame, width=450, height=50, fg_color="white", bg_color="white",
                                hover_color=green, border_color=green, border_width=2, text_color="black", corner_radius=10, text="Scrap", command=lambda: button_command())

        canvasTitle.pack()
        title.pack()
        separatorTitle.pack()
        departementMenu.pack()
        separatorOptionM.pack()
        numberEntry.pack()
        separatorNumber.pack()
        csvFileName.pack()
        separatorCSV.pack()
        tabName.pack()
        separatorTab.pack()
        fileName.pack()
        separatorFileName.pack()
        switchMailButton.pack()
        scrapButton.pack()

        topRevenueFrame.pack(pady=20)

    def ActivityPage():
        activityFrame = tk.Frame(main_frame, bg="white")

        canvasTitle = tk.Canvas(activityFrame, width=250, height=100, bg="white", highlightthickness=0)
        title = tk.Label(canvasTitle, text="Recherche à partir du domaine d'activité", font=("CenturyGothic", 24), fg="black", bg="white")

        separatorTitle = tk.Frame(activityFrame, height=40, width=450, bg="white")

        activity = tk.StringVar()
        activity.set("Activité administrative et autres services de soutien aux entreprises")

        departementMenu = CTkOptionMenu(activityFrame, width=450, height= 50, fg_color=green, button_color=green, button_hover_color=green,
                                        text_color="black", corner_radius=10, values=ActivityLinksKey, variable=activity)
        
        separatorOptionM = tk.Frame(activityFrame, height=40, width=450, bg="white")

        numberEntry = CTkEntry(activityFrame, width=450, height=50, border_color="white", fg_color=green,
                               text_color="black", corner_radius=10, placeholder_text="Nombre d'entreprise à scraper") 
        
        separatorNumber = tk.Frame(activityFrame, height=40, width=450, bg="white")

        csvFileName = CTkEntry(activityFrame, width=450, height=50, border_color="white", fg_color=green, 
                               text_color="black", corner_radius=10, placeholder_text="Nom du fichier csv")

        separatorCSV = tk.Frame(activityFrame, height=40, width=450, bg="white")

        tabName = CTkEntry(activityFrame, width=450, height=50, border_color="white", fg_color=green, 
                           text_color="black", corner_radius=10, placeholder_text="Nom du tableur")

        separatorTab = tk.Frame(activityFrame, height=40, width=450, bg="white")

        fileName = CTkEntry(activityFrame, width=450, height=50, border_color="white", fg_color=green,
                                 text_color="black", corner_radius=10, placeholder_text="Nom du fichier tableur")

        separatorFileName = tk.Frame(activityFrame, height=40, width=450, bg="white")

        switchMail = tk.BooleanVar()
        switchMail.set(False)
        switchMailButton = CTkSwitch(activityFrame, text="Recherches des mails ?", text_color="black", width=450, height=50,
                                    fg_color="red", bg_color="white", button_color="#DCDCDC", button_hover_color="#DCDCDC", variable=switchMail, corner_radius=10)

        def button_command():
            try:
                number = int(float(numberEntry.get()))
            except ValueError:
                messagebox.showerror("Error", "Le nombre de sociétés doit être un nombre")
                return
            return scrapActivity(ActivityLinks[activity.get()], number, csvFileName.get(), tabName.get(), fileName.get(), switchMail.get())

        scrapButton = CTkButton(activityFrame, width=450, height=50, fg_color="white", bg_color="white",
                                hover_color=green, border_color=green, border_width=2, text_color="black", corner_radius=10, text="Scrap", command=lambda: button_command())

        canvasTitle.pack()
        title.pack()
        separatorTitle.pack()
        departementMenu.pack()
        separatorOptionM.pack()
        numberEntry.pack()
        separatorNumber.pack()
        csvFileName.pack()
        separatorCSV.pack()
        tabName.pack()
        separatorTab.pack()
        fileName.pack()
        separatorFileName.pack()
        switchMailButton.pack()
        scrapButton.pack()

        activityFrame.pack(pady=20)

    def FilePage():
        fileFrame = tk.Frame(main_frame, bg="white")

        canvasTitle = tk.Canvas(fileFrame, width=250, height=100, bg="white", highlightthickness=0)
        title = tk.Label(canvasTitle, text="Recherche à partir d'un fichier existant", font=("CenturyGothic", 24), fg="black", bg="white")
        
        separatorTitle = tk.Frame(fileFrame, height=40, width=450, bg="white")


        switchAct = tk.BooleanVar()
        switchAct.set(False)
        switchActButton = CTkSwitch(fileFrame, text="Rouge : Revenue | Bleu : Activité", text_color="black", width=450, height=50, fg_color="red", bg_color="white",
                                 button_color="#DCDCDC", button_hover_color="#DCDCDC", variable=switchAct, corner_radius=10)

        separatorSwitchAct = tk.Frame(fileFrame, height=40, width=450, bg="white")

        def select_file(): 
            filetypes = [("CSV files", "*.csv")]

            fname = fd.askopenfilename(filetypes=filetypes, title='Choisir un fichier CSV', initialdir=csvPath)

            if fname:
                compactFileName = Path(fname).name
                fileEntry.configure(text=compactFileName)
        
        fileEntry = CTkButton(fileFrame, width=450, height=50, fg_color="white", bg_color="white",
                                hover_color=green, border_color=green, border_width=2, text_color="black", corner_radius=10, text="Choisir un fichier", command=select_file)
        
        separatorFile = tk.Frame(fileFrame, width=40, height=30, bg="white")

        numberEntry = CTkEntry(fileFrame, width=450, height=50, border_color="white", fg_color=green, text_color="black", 
                               corner_radius=10, placeholder_text="Nombre d'entreprise à scraper")

        separatorNumber = tk.Frame(fileFrame, width=40, height=250, bg="white")

        switchMail = tk.BooleanVar()
        switchMail.set(False)
        switchMailButton = CTkSwitch(fileFrame, text="Recherches des mails", text_color="black", width=450, height=50,
                                    fg_color="red", bg_color="white", button_color="#DCDCDC", button_hover_color="#DCDCDC", variable=switchMail, corner_radius=10)

        def button_command():
            try:
                number = int(float(numberEntry.get()))
                typeSearch: bool = switchAct.get()
            except ValueError:
                messagebox.showerror("Error", "Le nombre de sociétés doit être un nombre")
                return
            else: 
                filename = fileEntry.cget("text")
                return scrapFromFile(filename, number, typeSearch, switchMail.get())

        scrapButton = CTkButton(fileFrame, width=450, height=50, fg_color="white", bg_color="white",
                                hover_color=green, border_color=green, border_width=2, text_color="black", corner_radius=10, text="Scrap", command=lambda: button_command())

        canvasTitle.pack()
        title.pack()
        separatorTitle.pack()
        switchActButton.pack()
        separatorSwitchAct.pack()
        fileEntry.pack()
        separatorFile.pack()
        numberEntry.pack()
        separatorNumber.pack()
        switchMailButton.pack()
        scrapButton.pack()

        fileFrame.pack(pady=20)
    
    TopRevenuePage()

    root.mainloop()

def main():
    App()
    for file in Path(__file__).parent.joinpath("tmp_html").iterdir():
        file.unlink()

    
if __name__ == "__main__":
    main()
