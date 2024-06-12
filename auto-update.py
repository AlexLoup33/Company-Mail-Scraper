# __author__ = "Lou-Poueyou Alexandre | github.com/AlexLoup33"

"""
This script will update all the project if a new version is available
To do this, we will look at the version of the project on the github repository and compare it with the local version
If the version is different, we will update the project
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path

def getLatestRelease():
    """
    Get the latest release of the project on the github repository
    """
    url = "https://api.github.com/repos/AlexLoup33/Company-Mail-Scraper/releases/latest"
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        return json.loads(response.text)["tag_name"]
    else:
        return None
    
def updateProject():
    """
    Update the project to the latest version
    """
    # Get the latest release of the project
    latestRelease = getLatestRelease()
    if latestRelease is None:
        print("Error while getting the latest release of the project")
        sys.exit(1)
    
    # Get the current version of the project
    currentVersion = Path(__file__).parent.joinpath("version.txt").read_text()
    
    if latestRelease == currentVersion:
        print("The project is already up to date")
        sys.exit(0)
    
    # Update the project
    print("Updating the project to the latest version")
    os.system("git pull")
    Path(__file__).parent.joinpath("version.txt").write_text(latestRelease)
    print("The project has been updated to the latest version")

if __name__ == "__main__":
    updateProject()