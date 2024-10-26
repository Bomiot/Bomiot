from configparser import ConfigParser
from pathlib import Path
from os.path import join

config = ConfigParser()
config_path = Path(__file__).resolve().parent

def mode_return() -> str:
    config.read(join(config_path, 'config.ini'))
    feedback = config.get('mode', 'name', fallback='plugins')
    return feedback