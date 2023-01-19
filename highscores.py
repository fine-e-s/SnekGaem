import pickle
import requests


def get_file():
    return pickle.loads(requests.get('http://lance5021.pythonanywhere.com/get').content)


def write_file(entry):
    requests.post('http://lance5021.pythonanywhere.com/add', json=entry)
