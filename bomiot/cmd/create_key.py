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
        print('Auth key file created successfully. It will expire at 7 days.')
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
        print('Auth key file created successfully. It will expire at 7 days.')
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
            if pattern.match(line):
                prefix = pattern.match(line).group(1)
                if isinstance(new_key, str) and not new_key.isdigit():
                    value_str = f'"{new_key}"'
                else:
                    value_str = str(new_key)
                new_line = f"{prefix}{value_str}\n"
                new_lines.append(new_line)
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        f.close()
        print('Auth key refresh successfully. It will expire at 7 days.')
        print(f'new keys: {new_key}')
