import json


def open_json():
    with open("123.json", "r", encoding="utf-8") as f:
        table = json.load(f)
    return table

