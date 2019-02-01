# coding: utf-8
import csv

from pathlib import Path
from dotenv import load_dotenv


def get_dictsites(filename):
    dictsites = []
    with open(filename, 'rU') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            dictsites.append(row)
    return dictsites


def load_env_config():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path,
                verbose=True,
                override=False)
