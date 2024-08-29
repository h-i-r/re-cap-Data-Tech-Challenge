import json
import os

def read_json(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, 'r') as file:
        return json.load(file)