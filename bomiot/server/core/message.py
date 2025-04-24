from tomlkit import parse
from os.path import join, exists
from django.conf import settings


def permission_message_return(language: str, data: str) -> str:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        try:
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
            return message_data['permission'][data]
        except:
            return data
    else:
        return data


def detail_message_return(language: str, data: str) -> dict:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        try:
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
            return {'detail': message_data['detail'][data]}
        except:
            return {'detail': data}
    else:
        return {'detail': data}


def msg_message_return(language: str, data: str) -> dict:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        try:
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
            return {'msg': message_data['msg'][data]}
        except:
            return {'msg': data}
    else:
        return {'msg': data}

def login_message_return(language: str, data: str) -> dict:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        try:
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
            return {'login': message_data['login'][data]}
        except KeyError:
            return {'login': data}
    else:
        return {'login': data}

def others_message_return(language: str, data: str) -> str:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        try:
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
            return message_data['others'][data]
        except:
            return data
    else:
        return data
