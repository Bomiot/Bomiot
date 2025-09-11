import orjson
import ast
import aiofiles
import asyncio
import pandas as pd
from django.conf import settings
from os.path import join
import importlib.util
import importlib
from pathlib import Path
from bomiot_message import msg_message_return
import os
import shutil
import filecmp
from filecmp import dircmp

def get_job_id(task):
    """
    construct job id
    :return: job id
    """
    return f'{task.job_id}'


def bytes2str(data):
    """
    bytes2str
    :param data: origin data
    :return: str
    """
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    data = data.strip()
    return data


def load_dict(x, transformer=None):
    """
    convert to  dict
    :param x:
    :return:
    """
    if x is None or isinstance(x, dict):
        return x
    try:
        data = orjson.loads(x)
        if not transformer:
            def transformer(x): return x
        data = {k: transformer(v) for k, v in data.items()}
        return data
    except:
        return {}


def str2list(x, transformer=None):
    """
    convert to list
    :param x:
    :return:
    """
    if x is None or isinstance(x, list):
        return x
    try:
        data = orjson.loads(x)
        if not transformer:
            def transformer(x): return x
        data = list(map(lambda x: transformer(x), data))
        return data
    except:
        return []


def str2bool(v):
    """
    convert string to bool
    :param v:
    :return:
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    return True


def str2json(v):
    """
    convert str to json data
    :param v:
    :return:
    """
    try:
        return orjson.loads(v)
    except:
        return None


def str2dict(v):
    """
    convert str to dict data
    :param v:
    :return:
    """
    try:
        return orjson.loads(v)
    except:
        return {}


def str2body(v):
    """
    convert str to json data or keep original string
    :param v:
    :return:
    """
    try:
        return orjson.loads(v)
    except:
        return v


def str2str(v):
    """
    convert str to str, process for 'None', 'null', '',
    :param v:
    :return:
    """
    if v.lower() in ('none', 'null', 'undefined', 'nil', 'false'):
        return None
    return str(v)


def is_dict_empty(d):
    return not d.items()


def excel_to_json(path: str, skip=0, read_rows=31) -> list:
    df = pd.read_excel(path, nrows=0, header=0, engine='openpyxl')
    column_names = df.columns.tolist()
    df = pd.read_excel(path, skiprows=skip, nrows=read_rows, engine='openpyxl', names=column_names)
    data = df.to_json(orient="records", date_format="iso", date_unit='s', force_ascii=False)
    return orjson.loads(data)


def read_excel_title(path: str) -> list:
    df = pd.read_excel(path, nrows=0, header=0, engine='openpyxl')
    return df.columns.tolist()


def contains_value(data: dict, value) -> bool:
    return value in data.values()


def readable_file_size(size_in_bytes) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} EB"


def compare_dicts(dict1, dict2) -> dict:
    return {k: (dict1[k], dict2[k]) for k in dict1 if dict1[k] != dict2[k]}


def queryset_to_dict(queryset) -> list:
    """
    Convert a Django queryset to a list of dictionaries.
    :param queryset: Django queryset
    :return: List of dictionaries
    """
    return [{
        **flatten_json(obj),
        'created_time': obj['created_time'].strftime('%Y-%m-%d %H:%M:%S'),
        'updated_time': obj['updated_time'].strftime('%Y-%m-%d %H:%M:%S')
    } for obj in queryset.values('id', 'created_time', 'updated_time', 'data')]


def find_value_in_json(json_data, key_to_find):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == key_to_find:
                return value
            if isinstance(value, (dict, list)):
                result = find_value_in_json(value, key_to_find)
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_value_in_json(item, key_to_find)
            if result is not None:
                return result
    return None


def flatten_json(nested_dict):
    return {
        **nested_dict['data'],
        'id': nested_dict['id'],
        'created_time': nested_dict['created_time'],
        'updated_time': nested_dict['updated_time']
    }


def is_empty_value(val):
    if isinstance(val, dict):
        return all(is_empty_value(v) for v in val.values())
    elif isinstance(val, list):
        return all(is_empty_value(v) for v in val)
    return val in [None, '', 'null', 'undefined', 'nil', [], {}, set()]


def all_fields_empty(json_dict):
    return is_empty_value(json_dict)


def find_keys_by_value(dictionary, target_value):
    if dictionary is None:
        return [f'{target_value}']
    res = [key for key, value in dictionary.items() if value == target_value]
    if len(res) > 0:
        return res
    return [f'{target_value}']

def merge_and_filter_items(items):
    merged = {}
    for item in items:
        if not item.get('selected') or not item.get('qty'):
            continue
        qty = str(item['qty']).strip()
        if not qty:
            continue
        key = frozenset(item['selected'].items())
        if key in merged:
            merged[key]['qty'] = str(float(merged[key]['qty']) + float(qty))
        else:
            new_item = item.copy()
            new_item['qty'] = qty
            merged[key] = new_item
    return list(merged.values())

def check_method_in_file_by_ast(file_path, method_name):
    try:
        detail = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
        found = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == method_name and isinstance(tree, ast.Module):
                    detail = {
                                "class": node.name,
                                "method": method_name,
                            }
                    found = True
                    break
            elif isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if item.name == method_name:
                            detail = {
                                "class": node.name,
                                "method": method_name,
                            }
                            found = True
                            break
                if found:
                    break
        return found, detail

    except FileNotFoundError:
        print(f"'{file_path}' can not find")
        return False, detail
    except SyntaxError as e:
        print(f"'{file_path}' {e}")
        return False, detail
    except Exception as e:
        print(f"{e}")
        return False, detail

def receiver_callback(data, method) -> dict:
    project_name = data.get('request').COOKIES.get('project', settings.PROJECT_NAME)
    if project_name.lower() == 'bomiot':
        receiver_path = join(settings.WORKING_SPACE, settings.PROJECT_NAME, 'receiver.py')
    else:
        receiver_path = join(settings.WORKING_SPACE, project_name, 'receiver.py')
    receiver_check = check_method_in_file_by_ast(receiver_path, method)
    if receiver_check[0] is True:
        spec = importlib.util.spec_from_file_location("receiver", receiver_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if 'class' in receiver_check[1]:
            try:
                target_class = getattr(module, receiver_check[1]['class'])
                instance = target_class()
                if hasattr(instance, receiver_check[1]['method']):
                    result = getattr(instance, receiver_check[1]['method'])(data)
                    return result
                else:
                    print(f"{type(receiver_check[1]).get('class')} class don't have {receiver_check[1]['method']} method")
            except AttributeError:
                print(f"class {type(receiver_check[1]).get('class')} can not find {receiver_path}")
        else:
            if hasattr(module, receiver_check[1]['method']):
                result = getattr(module, receiver_check[1]['method'])(data)
                return result
            else:
                print(f"{receiver_path} don't have {receiver_check[1]['method']} method")
    else:
        mode = data.get('mode')
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        if mode == 'get':
            return [
            ('results', data.get('data')),
        ]
        elif mode == 'create':
            return msg_message_return(language, "Success Create")
        elif mode == 'update':
            return msg_message_return(language, "Success Update")
        elif mode == 'delete':
            return msg_message_return(language, "Success Delete")
               
async def async_write_file(file_path, file_data):
    """
    Async write file
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_data)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {str(e)}")
        return False

def sync_write_file(file_path, file_data):
    """
    Sync use asyncio to async write file
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(async_write_file(file_path, file_data))
        return result
    finally:
        loop.close()


def are_folders_identical(folder1, folder2, subfolder_path='dist', print_log=True):
    """
    mirror templates
    """
    subfolder1 = os.path.join(folder1, subfolder_path)
    subfolder2 = os.path.join(folder2, subfolder_path)
    for subfolder in [subfolder1, subfolder2]:
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
    def _sync_subdirs(dcmp):
        for item in dcmp.funny_files:
            src = os.path.join(dcmp.left, item)
            dest = os.path.join(dcmp.right, item)
            if os.path.exists(dest):
                if os.path.isfile(dest):
                    os.remove(dest)
                else:
                    shutil.rmtree(dest)
            if os.path.isfile(src):
                shutil.copy2(src, dest)
            else:
                shutil.copytree(src, dest)
        for item in dcmp.right_only:
            path = os.path.join(dcmp.right, item)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        for item in dcmp.left_only:
            src = os.path.join(dcmp.left, item)
            dest = os.path.join(dcmp.right, item)
            if os.path.isfile(src):
                shutil.copy2(src, dest)
            else:
                shutil.copytree(src, dest)
        for item in dcmp.diff_files:
            src = os.path.join(dcmp.left, item)
            dest = os.path.join(dcmp.right, item)
            shutil.copy2(src, dest)
        for sub_dcmp in dcmp.subdirs.values():
            _sync_subdirs(sub_dcmp)
    dcmp = dircmp(subfolder1, subfolder2)
    _sync_subdirs(dcmp)
    final_dcmp = dircmp(subfolder1, subfolder2)
    is_identical = not (final_dcmp.left_only or final_dcmp.right_only or 
                       final_dcmp.diff_files or final_dcmp.funny_files)
    return is_identical

def dynamic_import_and_call(module_path, function_name, *args, **kwargs):
    """
    Dynamically import a method from a module and execute it.

    Args:
        module_path (str): The path of the module, e.g. 'my_module.my_functions'.
        function_name (str): The name of the method, e.g. 'greet_person'.
        *args: Positional arguments to pass to the method.
        **kwargs: Keyword arguments to pass to the method.

    Returns:
        any: The return value of the called method.
    """
    try:
        module = importlib.import_module(module_path)
        func = getattr(module, function_name)
        result = func(*args, **kwargs)
        return result
    except ImportError:
        print(f"Error: Module '{module_path}' could not be imported.")
        return None
    except AttributeError:
        print(f"Error: Function '{function_name}' not found in module '{module_path}'.")
        return None