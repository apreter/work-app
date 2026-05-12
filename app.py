import requests
import subprocess
import sys
import os
import time
import random
import msvcrt

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
    except:
        pass

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

# Snake spēle
WIDTH = 40
HEIGHT = 20

def clear():
    os.system('cls')

def draw(snake, food, score):
    board = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x, y in snake:
        if 0 <= y < HEIGHT and 0 <= x < WIDTH:
            board[y][x] = '#'
    fx, fy = food
    board[fy][fx] = '*'
    clear()
    print(f"  Snake | Punkti: {score}")
    print("  " + "-" * WIDTH)
    for row in board:
        print("  |" + "".join(row) + "|")
    print("  " + "-" * WIDTH)
    print("  Vadība: W A S D | Q = iziet")

def game():
    snake = [(WIDTH//2, HEIGHT//2)]
    direction = (1, 0)
    food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
    score = 0
    speed = 0.15

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'w' and direction != (0, 1):
                direction = (0, -1)
            elif key == 's' and direction != (0, -1):
                direction = (0, 1)
            elif key == 'a' and direction != (1, 0):
                direction = (-1, 0)
            elif key == 'd' and direction != (-1, 0):
                direction = (1, 0)
            elif key == 'q':
                print("Izeja...")
                sys.exit()

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake):
            clear()
            print(f"\n  SPĒLE BEIGUSIES! Punkti: {score}")
            print("  Nospied jebkuru taustiņu...")
            msvcrt.getch()
            break

        snake.insert(0, head)

        if head == food:
            score += 1
            food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
            speed = max(0.05, speed - 0.005)
        else:
            snake.pop()

        draw(snake, food, score)
        time.sleep(speed)

check_update()
game()