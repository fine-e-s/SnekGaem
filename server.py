from flask import Flask, request
from datetime import datetime
import pickle
from pathlib import Path

HIGHSCORES_FILE = Path('/home/lance5021/mysite/records.records')

app = Flask(__name__)
highscores_list = []


def get_template():
    return [{'place': f'{i}', 'name': '---', 'score': 0,
             'time': get_current_time()} for i in range(1, 11)]


def reset():
    with open(HIGHSCORES_FILE, 'wb') as file:
        pickle.dump(get_template(), file)
    file.close()
    open_file()


def get_current_time():
    return str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '').replace('.', '')


def open_file():
    global highscores_list
    if HIGHSCORES_FILE.exists():
        with open(HIGHSCORES_FILE, 'rb') as file:
            highscores_list = pickle.load(file)
        file.close()
    else:
        reset()


def submit_score(data):
    global highscores_list
    data.update({'time': get_current_time()})
    highscores_list.append(data)

    highscores_list = sorted(sorted(
        highscores_list, key=lambda d: d['time'], reverse=True),
        key=lambda e: e['score'], reverse=True
    )

    highscores_list = highscores_list[:10]

    for place, entry in enumerate(highscores_list):
        entry.update({'place': str(place + 1)})

    with open(HIGHSCORES_FILE, 'wb') as file:
        pickle.dump(highscores_list, file)
        file.close()


@app.route('/get')
def get_scores():
    open_file()
    return pickle.dumps(highscores_list)


@app.route('/add', methods=['POST'])
def add_entry():
    submition = request.get_json()
    submit_score(submition)
