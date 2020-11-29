import os
import json


def read_json(file_name):
    with open(file_name, 'r', encoding="utf8") as read_file:
        return json.load(read_file)
