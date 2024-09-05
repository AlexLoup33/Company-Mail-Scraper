__author__ = "Lou-Poueyou Alexandre | github.com/AlexLoup33"

import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package]) # type: ignore

if __name__ == "__main__":
    install("beautifulsoup4")
    install("openpyxl")
    install("requests")
    install("tk")
    install("customtkinter")
    install("pillow")
    install("aiohttp")
    install("validators")
    install("wget")
    install("selenium")
    install("python-whois")
    install("customtkinter")
    install("python-dotenv")