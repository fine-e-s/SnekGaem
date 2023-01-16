from datetime import datetime
import pickle
from pathlib import Path

HIGHSCORES_FILE = Path('records.records')


def get_current_time():
    return str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '').replace('.', '')


class Highscores:
    def __init__(self):
        self.highscores_list = None
        self.get_file()

    def get_file(self):
        if HIGHSCORES_FILE.exists():
            with open(HIGHSCORES_FILE, 'rb') as file:
                self.highscores_list = pickle.load(file)
            file.close()
        else:
            self.reset()

    def reset(self):
        with open(HIGHSCORES_FILE, 'wb') as file:
            pickle.dump(self.get_template(), file)
        file.close()
        self.get_file()

    def get_template(self):
        return [{'place': f'{i}', 'name': '---', 'score': 0, 'time': get_current_time()} for i in range(1, 11)]

    def write_file(self):
        with open(HIGHSCORES_FILE, 'wb') as file:
            pickle.dump(self.highscores_list, file)
        file.close()
        self.get_file()
