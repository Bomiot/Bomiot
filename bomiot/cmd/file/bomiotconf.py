from configparser import ConfigParser


config = ConfigParser()


def mode_return() -> str:
    config.read('.config.ini')
    return config.get('mode', 'name', fallback='plugins')