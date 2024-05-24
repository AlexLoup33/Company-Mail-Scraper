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
    install("aiohttp")
    install("validators")
    install("wget")
    install("selenium")