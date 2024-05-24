import requests
import validators
import socket

from bs4 import BeautifulSoup
from typing import NamedTuple
from selenium import webdriver

class NetworkScrap(NamedTuple):
    contactPage: str
    facebook: str
    twitter: str
    linkedin: str

def findNetwork(url:str)->"NetworkScrap":
    """
    Get the html page of the url and scrap the page to find the network of the company
    The function will try to find the contact page, Facebook, Twitter and LinkedIn of the company
    Some element can be missing if the company doesn't have a page on the social network or
    hide it from the public, in this case, the element will be "Non disponible".
    Must also check if the url contain https or http, if not, the function will add it because
    requests need it to work properly.
    """
    if not url.startswith("www"):
        url = "www." + url
    if not (url.startswith("http") or url.startswith("https")):
        if isValidPage("https://" + url):
            url = "https://" + url
        elif isValidPage("http://" + url):
            url = "http://" + url
        else:
            assert("The url is not valid, please check the url manually")

    if not isValidPage(url):
        print("The domain is not valid, please check the url manually")
        return None
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    """
    The parser search for the iteration of the word "contact" in the <href> tag in the
    html page, if the word is found, the parser will return the link of the contact page
    The parser can find more than one link, in this case, use a list and store all of them.
    """
    contactPage = None
    for link in soup.find_all('a', href=True):
        if 'contact' in link.get('href') or 'contact' in link.get_text():
            contactPage = link.get('href')

    """
    Must verify with the `if contactPage` if the return of find_all is not None
    If the return is None then let the value of contactPage to None, the program will
    handle the case where the contact page is not found and replace it with "Non disponible"
    when the NetworkScrap is created.
    """
    if contactPage and not (contactPage.startswith("http") or contactPage.startswith("https") or contactPage.startswith("www")):
        contactPage = url + contactPage
    if contactPage and not isValidPage(contactPage):
        contactPage = refactorUrl(contactPage)

    links = soup.find_all('a', href=True)

    facebook = None
    twitter = None
    linkedin = None

    for link in links:
        href = link['href']
        if "facebook" in href:
            facebook = href
        elif "twitter" in href:
            twitter = href
        elif "linkedin" in href:
            linkedin = href
        else : #case where no social network are found
            pass


    print(f"Contact page: {contactPage}")
    print(f"Facebook: {facebook}")
    print(f"Twitter: {twitter}")
    print(f"LinkedIn: {linkedin}")

    looped: bool = False
    while (not facebook and not twitter and not linkedin):
        driver = webdriver.Chrome()
        driver.get(url)

        source_page = driver.page_source
        with open('tmp_html/'+getCompanyName(url)+'.html', 'w') as f:
            f.write(source_page)
    
        driver.quit()

        """
        The html page is already saved in the tmp_html folder, now we open the file and retry
        to find the informations desired (hope i found lmao)
        """

        with open('tmp_html/'+getCompanyName(url)+'.html', 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

            links = soup.find_all('a', href=True)

            for link in links:
                href = link['href']
                if "facebook" in href:
                    facebook = href
                elif "twitter" in href:
                    twitter = href
                elif "linkedin" in href:
                    linkedin = href
                elif "contact" in href and not contactPage:
                    contactPage = href
                else :
                    pass
        if looped or (facebook or twitter or linkedin):
            break
        looped = True
    
    print("Post traitement")
    print(f"Contact page: {contactPage}")
    print(f"Facebook: {facebook}")
    print(f"Twitter: {twitter}")
    print(f"LinkedIn: {linkedin}")

    return NetworkScrap(contactPage, facebook, twitter, linkedin)


"""
Refactor the url by changing his extension because the url isn't valid
Will test with a lot of extension to find a valid one
"""
def refactorUrl(url:str)->str|None:
    if isValidPage(url):
        return url
    
    domainExtension = [".com", ".fr", ".org", ".net", ".edu", ".gov"] #ざさつばく

    # Try to replace the url extension with all the extension since the url is invalid
    for extension in domainExtension:
        for e in domainExtension:
            if extension in url and e not in url:
                url = url.replace(extension, e)
                if isValidPage(url):
                    return url
    
    return None


"""
Check if the page is still online and accessible
Allow then to scrap the page or looking if the scraping is still possible
If not, the program return false and a solution for searching the page will be proposed (or not)
"""
def isValidPage(url:str)->bool:
    try :
        ip = validators.url(url)
        return True
    except validators.ValidationFailure:
        return False


def getCompanyName(url:str)->str:
    """
    Only get the name of the company from the url by removing the extension and the "www." is it's present
    Not essential but allow to make a clean name file for the copy of the /robots.txt of the company
    """
    if "www." in url:
        return url.split(".")[1]
    return url.split(".")[0]


def verifDNS(domain:str)->bool:
    try:
        ip = socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def main():
    url = "www.cdiscount.com"
    findNetwork(url)

if __name__ == "__main__":
    main()