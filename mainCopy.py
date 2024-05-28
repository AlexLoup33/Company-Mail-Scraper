__author__ = "AlexLoup33 | github.com/AlexLoup33"

import tkinter as tk

from scrapper import scrap, departementLinks
from pathlib import Path

light_gray = "#FAFAFA"
green = "#AEEEE0"

logoPath = Path(__file__).parent.joinpath("res")

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
    """
    #Create a graphic interface
    root = tk.Tk()
    root.title("Saine Mail Scrapper")
    root.geometry("500x500")
    root.resizable(True, True)

    #Create a label
    label = tk.Label(root, text="Saine Mail Scrapper", font=("Arial", 15))
    label.pack()

    #Create a margin
    margin = tk.Label(root, text="")
    margin.pack()

    #Create a combobox for the department, the program will take the value in the dict according to the department selected
    departmentLabel = tk.Label(root, text="Département concerné")
    departmentLabel.pack()

    department = tk.StringVar()
    department.set("Ain")
    departmentMenu = tk.OptionMenu(root, department, *departementLinks.keys())
    departmentMenu.pack()

    #Create a slider for the number of companies who start from 1 to the number of companies
    sliderLabel = tk.Label(root, text="Nombre d'entreprise à scraper")
    sliderLabel.pack()
    slider = tk.Entry(root, width=50)
    slider.pack()



    #Create an input for the name of the file csv
    csvLabel = tk.Label(root, text="Nom du fichier csv")
    csvLabel.pack()
    name_csv = tk.Entry(root, width=50)
    name_csv.pack()

    #Create an input for the name of the tabsheet
    tabLabel = tk.Label(root, text="Nom du tableur")
    tabLabel.pack()
    name_tab = tk.Entry(root, width=50)
    name_tab.pack()

    #Create an input for the name of the file tabsheet
    fileLabel = tk.Label(root, text="Nom du fichier tableur")
    fileLabel.pack()
    name_file = tk.Entry(root, width=50)
    name_file.pack()

    def button_func():
        try:
            number = int(float(slider.get()))
        except ValueError:
            messagebox.showerror("Error", "Le nombre de sociétés doit être un nombre")
            return
        return scrap(departementLinks[department.get()], number, name_csv.get(), name_tab.get(), name_file.get())

    #Create a button that scrap the companies, make a label appear when the function is done 
    button = tk.Button(root, text="Scrap", command=button_func)
    button.pack(pady=10)

    root.mainloop()
    """
    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(False, False)
    root.title("Company Mail Scapper")

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
        topRevenueFrame = tk.Frame(main_frame)

        canvasTitle = tk.Canvas(topRevenueFrame, width=250, height=100, bg="white", highlightthickness=0)
        title = tk.Label(canvasTitle, text="Recherche à partir des revenues", font=("CenturyGothic", 24), fg="black", bg="white")
        
        canvasTitle.pack()
        title.pack()

        topRevenueFrame.pack(pady=20)

    def ActivityPage():
        activityFrame = tk.Frame(main_frame)

        canvasTitle = tk.Canvas(activityFrame, width=250, height=100, bg="white", highlightthickness=0)
        title = tk.Label(canvasTitle, text="Recherche à partir du domaine d'activité", font=("CenturyGothic", 24), fg="black", bg="white")
        canvasTitle.pack()
        title.pack()

        activityFrame.pack(pady=20)

    def FilePage():
        fileFrame = tk.Frame(main_frame)

        canvasTitle = tk.Canvas(fileFrame, width=250, height=100, bg="white", highlightthickness=0)
        title = tk.Label(canvasTitle, text="Recherche à partir d'un fichier existant", font=("CenturyGothic", 24), fg="black", bg="white")
        canvasTitle.pack()
        title.pack()

        fileFrame.pack(pady=20)
    root.mainloop()


def main():
    App()

if __name__ == "__main__":
    main()