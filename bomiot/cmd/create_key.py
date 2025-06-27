import re
from bomiot_token import encrypt_info

from os.path import join, exists 
from os import getcwd

def auth_key_get():
    path = join(getcwd(), 'auth_key.py')
    if not exists(join(path)):
        while True:
            key_code = encrypt_info()
            if '/' in key_code:
                continue
            else:
                break
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'KEY = "{key_code}"\n')
        f.close()
        print(f'keys: {key_code}')

def auth_key_refresh():
    path = join(getcwd(), 'auth_key.py')
    if not exists(join(path)):
        while True:
            key_code = encrypt_info()
            if '/' in key_code:
                continue
            else:
                break
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'KEY = "{key_code}"\n')
        f.close()
        print(f'keys: {key_code}')
    else:
        while True:
            new_key = encrypt_info()
            if '/' in new_key:
                continue
            else:
                break
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        pattern = re.compile(rf"^(\s*KEY\s*=\s*)(.*)$")
        new_lines = []
        for line in lines:
            print(pattern.match(line))
            if pattern.match(line):
                prefix = pattern.match(line).group(1)
                if isinstance(new_key, str) and not new_key.isdigit():
                    value_str = f'"{new_key}"'
                else:
                    value_str = str(new_key)
                new_line = f"{prefix}{value_str}\n"
                new_lines.append(new_line)
        if len(new_lines) == 0:
            if isinstance(new_key, str) and not new_key.isdigit():
                value_str = f'"{new_key}"'
            else:
                value_str = str(new_key)
            new_lines.append(f'KEY = {value_str}\n')
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        f.close()
        print(f'new keys: {new_key}')


def auth_key_force():
    path = join(getcwd(), 'auth_key.py')
    if not exists(join(path)):
        while True:
            key_code = encrypt_info()
            if '/' in key_code:
                continue
            else:
                break
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'KEY = "{key_code}"\n')
        f.close()
        return key_code
    else:
        while True:
            new_key = encrypt_info()
            if '/' in new_key:
                continue
            else:
                break
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        pattern = re.compile(rf"^(\s*KEY\s*=\s*)(.*)$")
        new_lines = []
        for line in lines:
            if pattern.match(line):
                prefix = pattern.match(line).group(1)
                if isinstance(new_key, str) and not new_key.isdigit():
                    value_str = f'"{new_key}"'
                else:
                    value_str = str(new_key)
                new_line = f"{prefix}{value_str}\n"
                new_lines.append(new_line)
        if len(new_lines) == 0:
            if isinstance(new_key, str) and not new_key.isdigit():
                value_str = f'"{new_key}"'
            else:
                value_str = str(new_key)
            new_lines.append(f'KEY = {value_str}\n')
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        f.close()
        return new_key
