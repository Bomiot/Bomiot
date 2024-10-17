import importlib.util

def pkg_check(package, module):
    """
    check installed packages
    :return:
    """
    # TODO: Implement package check
    module_path = importlib.util.find_spec(f'{package}.{module}')
    return module_path is not None