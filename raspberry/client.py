import requests

import time

import os

import subprocess



SERVER_URL = "http://10.192.104.28:8000"

LECTEUR_ID = 1

BASE_PATH = "/home/admin/musique"



def jouer_pub(nom_fichier):

    chemin = os.path.join(BASE_PATH, "pub", nom_fichier)

    subprocess.run(["pkill", "-STOP", "mpv"])

    subprocess.run(["mpv", "--no-video", "--ao=alsa", chemin])

    subprocess.run(["pkill", "-CONT", "mpv"])



last_pl = None

while True:

    try:

        r = requests.get(f"{SERVER_URL}/api/ping/{LECTEUR_ID}", timeout=5)

        data = r.json()

        pl = data.get("playlist", "matin")

        if pl != last_pl:

            subprocess.run(["pkill", "-9", "mpv"])

            subprocess.Popen(["mpv", "--no-video", "--loop-playlist", "--shuffle", f"--playlist={os.path.join(BASE_PATH, pl)}"])

            last_pl = pl

        fichier = data.get("emplacement")

        if fichier:

            jouer_pub(fichier)

            requests.get(f"{SERVER_URL}/api/pub_terminee/{LECTEUR_ID}")



    except Exception as e:

        print(f"Erreur: {e}")

    time.sleep(5)