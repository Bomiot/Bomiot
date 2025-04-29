import orjson
import pandas as pd


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
