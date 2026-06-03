import json
import os


def load_materi():
    file_path = os.path.join("data", "materi_ekosistem.json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data