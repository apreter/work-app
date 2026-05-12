import requests
import subprocess
import sys

CURRENT_VERSION = "1.0.0"
GITHUB_USER = "apreter"
GITHUB_REPO = "work-app"

def check_update():
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
    try:
        latest = requests.get(url).text.strip()
        if latest != CURRENT_VERSION:
            print(f"Atjauninājums: {latest}")
            download_update(latest)
        else:
            print("Versija ir jaunākā!")
    except:
        print("Nav interneta savienojuma")

def download_update(version):
    url = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/download/v{version}/app.exe"
    r = requests.get(url, stream=True)
    with open("app_new.exe", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    bat = "@echo off\ntimeout /t 2 /nobreak\nmove /y app_new.exe app.exe\nstart app.exe\ndel updater.bat"
    with open("updater.bat", "w") as f:
        f.write(bat)
    subprocess.Popen("updater.bat", shell=True)
    sys.exit()

check_update()
print("Programma darbojas!")