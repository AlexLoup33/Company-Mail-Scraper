import requests
import tkinter as tk

from pathlib import Path
from bs4 import BeautifulSoup
from typing import NamedTuple
from openpyxl import Workbook
from openpyxl.worksheet._read_only import ReadOnlyWorksheet 
from openpyxl.chartsheet.chartsheet import Chartsheet
from tkinter import messagebox
from time import sleep

class EmailScrap(NamedTuple):
    email: str
    score: int

class InfoScrap(NamedTuple):
    company_name: str
    domain: str
    email : EmailScrap | None

class Queue:
    def __init__(self, size:int):
        self.queue = []
        self.size:int = size+1
        self.pointer:int = 0

    def enqueue(self, item):
        if self.is_full():
            return None
        self.queue.append(item)
        self.pointer += 1

    def dequeue(self):
        if self.is_empty():
            return None
        self.pointer -= 1
        return self.queue.pop(0)
    
    def is_empty(self):
        return self.pointer <= 0
    
    def is_full(self):
        return self.pointer == self.size

companies_names_scrap: "list[str]" = [] #will contain all the companies names on verif.com
companies_link_scrap: "list[str]" = [] #will contain all the companies link on verif.com
companies_domains_scrap: "list[str]" = [] #will contain all the companies domain on verif.com
companies_emails_scrap: "list[EmailScrap | None]" = [] #will contain all the companies emails

api_key = "d4d29913091c9954368733ea3f29bbced2a8c63e"

csvPath = Path(__file__).parent.joinpath("save")
tabPath = Path(__file__).parent.joinpath("savetab")

# Create the directory if they don't exist
if not csvPath.exists():
    csvPath.mkdir()
if not tabPath.exists():
    tabPath.mkdir()

def scrap(url:str, number:int, 
          csvname:str, tabname:str, tabfilename:str)->None:
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all the company names and link to their page in a dictionary
    companies = soup.find_all('tr', class_="MuiBox-root css-1vaqj3c")
    maxCompanies = len(companies)

    size = (maxCompanies if number > maxCompanies 
            else number)

    # get the number names of companies the user wants
    for i in range(size):
        print(f"iteration : {i}", end="\n")
        company_name = companies[i].find('h3').text.strip()
        companies_names_scrap.append(company_name)
        company_link = companies[i].find('a')['href']

        # Combine the link with the base url to get the full link
        full_link = "https://www.verif.com" + company_link
        companies_link_scrap.append(full_link)
    
    # Get the domain name of each company
    for i in range(len(companies_link_scrap)):
        response = requests.get(companies_link_scrap[i])
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            # Take the text in the <a> in the span with class="MuiTypography-root MuiTypography-bodySmallMedium css-1ymqwc8"
            foundElement = soup.find('span', class_="MuiTypography-root MuiTypography-bodySmallMedium css-1ymqwc8")
            assert foundElement is not None
            domain = foundElement.text

            companies_domains_scrap.append(domain)
        except:
            companies_domains_scrap.append("No domain available")
            print("Domaine de l'entreprise: Non disponible", end="\n\n")

    with open(csvPath.joinpath(f"{csvname}.csv"), "w") as f:
        f.write("Company Name, Domain\n")
        for i in range(len(companies_names_scrap)):
            sleep(0.001)
            try:
                f.write(f"{companies_names_scrap[i]}, {companies_domains_scrap[i]}\n")
            except:
                pass
    
    # request type : https://api.hunter.io/v2/domain-search?domain=test.com&api_key=d4d29913091c9954368733ea3f29bbced2a8c63e
    # Get the email of each company
    for i in range(len(companies_domains_scrap)):
        domain = companies_domains_scrap[i]

        # optimise moi ça avec de l'asynchrone pour une version supérieur pour effectuer plusieurs appels en parralèle et gagner du temps
        response = requests.get(f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}") 
        responseData = response.json() 
        
        try:
            # get the first email with the highest score and his score and store them
            email = responseData['data']['emails'][0]['value']
            score = responseData['data']['emails'][0]['confidence']
            score = 0
        except (IndexError, KeyError):
            emailScrap = None
            print(f"skip the company {companies_names_scrap[i]} because the email is not available")
        else: emailScrap = EmailScrap(email, score)
        companies_emails_scrap.append(emailScrap)
            

    # Generate a tabsheet file with the companies names, domain and all the email with the score of the email store in the companies_... list
    wb = Workbook()
    ws = wb.active
    assert ws is not None

    ws.title = tabname
    assert not isinstance(ws, (ReadOnlyWorksheet, Chartsheet))

    data: "list[InfoScrap]" = []
    for i in range(len(companies_names_scrap)):
        emailScrap = companies_emails_scrap[i]
        if emailScrap is None:
            print(f"Email company {companies_names_scrap[i]} not found")
        data.append(InfoScrap(companies_names_scrap[i], companies_domains_scrap[i], emailScrap))

    ws.append(["Entreprise", "Nom de Domaine", "Email", "Score"])
    for row in data:
        email = row.email
        if email is None:
            mail = "Email non disponible"
            score = "Score non disponible"
        else:
            mail = email.email
            score = email.score
        ws.append([row.company_name, row.domain,mail, score]) 

    wb.save(tabPath.joinpath(f"{tabfilename}.xlsx"))

    messagebox.showinfo("Information", "Le tableur et le csv ont été créé avec succès")

def main():
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

    #Create an input for the url
    urlLabel = tk.Label(root, text="Url")
    urlLabel.pack()
    url = tk.Entry(root, width=50)
    url.pack()

    #Create a slider for the number of companies who start from 1 to the number of companies
    sliderLabel = tk.Label(root, text="Number of companies")
    sliderLabel.pack()
    slider = tk.Entry(root, width=50)
    slider.pack()



    #Create an input for the name of the file csv
    csvLabel = tk.Label(root, text="Name of the csv file")
    csvLabel.pack()
    name_csv = tk.Entry(root, width=50)
    name_csv.pack()

    #Create an input for the name of the tabsheet
    tabLabel = tk.Label(root, text="Name of the tabsheet")
    tabLabel.pack()
    name_tab = tk.Entry(root, width=50)
    name_tab.pack()

    #Create an input for the name of the file tabsheet
    fileLabel = tk.Label(root, text="Name of the file tabsheet")
    fileLabel.pack()
    name_file = tk.Entry(root, width=50)
    name_file.pack()

    def button_func():
        try:
            number = int(float(slider.get()))
        except ValueError:
            messagebox.showerror("Error", "Le nombre de sociétés doit être un nombre")
            return
        return scrap(url.get(), number, name_csv.get(), name_tab.get(), name_file.get())

    #Create a button that scrap the companies, make a label appear when the function is done 
    button = tk.Button(root, text="Scrap", command=button_func)
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()