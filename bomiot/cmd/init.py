from os.path import join, exists
from os import makedirs, getcwd
import shutil
from pathlib import Path
from tomlkit import parse, dumps
from bomiot.cmd.welcome import welcome
import logging
import colorama
from colorama import Fore, Style
from configparser import ConfigParser

colorama.init()


def create_file(folder: str = ''):
    """
        Create initial files and directories for the project
        :param folder: Target folder name (optional)
        :return: True if successful, False otherwise
    """
    try:
        working_space = getcwd()
        file_path = join(Path(__file__).resolve().parent, 'file')
        
        # Create pyproject.toml if it doesn't exist
        if not exists(join(working_space, 'pyproject.toml')):
            pyproject_source = join(file_path, 'pyproject.toml')
            if exists(pyproject_source):
                with open(pyproject_source, 'r', encoding='utf-8') as pip_file:
                    content = pip_file.read()
                    deploy_pip = parse(content)
                
                # Access the poetry section and modify it
                tool_section = deploy_pip.get('tool', {})
                if hasattr(tool_section, '__contains__') and 'poetry' in tool_section:
                    poetry_section = tool_section['poetry']
                else:
                    poetry_section = {}
                    tool_section['poetry'] = poetry_section
                
                poetry_section['name'] = folder if folder else 'bomiot'
                poetry_section['version'] = '0.0.1'
                
                deploy_pip['tool'] = tool_section
                    
                with open(join(working_space, 'pyproject.toml'), 'w', encoding='utf-8') as user_pip_file:
                    user_pip_file.write(dumps(deploy_pip))
            else:
                logging.warning(f"Source pyproject.toml not found at {pyproject_source}")

        # Generate auth key

        # Copy other essential files
        files_to_copy = [
            ('.gitignore', '.gitignore'),
            ('LICENSE', 'LICENSE'),
            ('launcher.py', 'launcher.py'),
            ('discovered_apps.py', 'discovered_apps.py'),
            ('logo.icns', 'logo.icns'),
            ('logo.png', 'logo.png'),
            ('logo.ico', 'logo.ico'),
            ('splash.png', 'splash.png'),
            ('sqlite3.def', 'sqlite3.def'),
            ('sqlite3.dll', 'sqlite3.dll'),
            ('README.md', 'README.md')
        ]
        
        for source_file, dest_file in files_to_copy:
            source_path = join(file_path, source_file)
            dest_path = join(working_space, dest_file)
            if not exists(dest_path) and exists(source_path):
                try:
                    shutil.copy2(source_path, dest_path)
                except Exception as e:
                    logging.error(f"Failed to copy {source_file}: {str(e)}")

        # Copy the greaterwms folder if it exists
        greaterwms_source = join(file_path, 'greaterwms')
        greaterwms_dest = join(working_space, 'greaterwms')
        if exists(greaterwms_source) and not exists(greaterwms_dest):
            try:
                shutil.copytree(greaterwms_source, greaterwms_dest)
                print(f"{Fore.BLUE}Copied 'greaterwms' folder to project.{Style.RESET_ALL}")
            except Exception as e:
                logging.error(f"Failed to copy 'greaterwms' folder: {str(e)}")

        # Copy the greaterwms2 folder if it exists
        greaterwms2_source = join(file_path, 'greaterwms2')
        greaterwms2_dest = join(working_space, 'greaterwms2')
        if exists(greaterwms2_source) and not exists(greaterwms2_dest):
            try:
                shutil.copytree(greaterwms2_source, greaterwms2_dest)
                print(f"{Fore.BLUE}Copied 'greaterwms2' folder to project.{Style.RESET_ALL}")
            except Exception as e:
                logging.error(f"Failed to copy 'greaterwms2' folder: {str(e)}")

        # Copy task.py to greaterwms directory
        task_source = join(file_path, 'task.py')
        task_dest = join(working_space, 'greaterwms', 'task.py')
        if exists(task_source) and not exists(task_dest):
            try:
                shutil.copy2(task_source, task_dest)
                print(f"{Fore.BLUE}Copied 'task.py' to greaterwms folder.{Style.RESET_ALL}")
            except Exception as e:
                logging.error(f"Failed to copy 'task.py': {str(e)}")

                # Copy the bomiot_test folder if it exists
            bomiot_test_source = join(file_path, 'bomiot_test')
            bomiot_test_dest = join(working_space, 'bomiot_test')
            if exists(bomiot_test_source) and not exists(bomiot_test_dest):
                try:
                    shutil.copytree(bomiot_test_source, bomiot_test_dest)
                    print(f"{Fore.BLUE}Copied 'bomiot_test' folder to project.{Style.RESET_ALL}")
                except Exception as e:
                    logging.error(f"Failed to copy 'bomiot_test' folder: {str(e)}")

        # Handle setup.ini: copy if it doesn't exist, or check and update if it does
        setup_ini_dest = join(working_space, 'setup.ini')
        setup_ini_source = join(file_path, 'setup.ini')
        
        if not exists(setup_ini_dest):
            # Copy setup.ini if it doesn't exist in destination
            if exists(setup_ini_source):
                shutil.copy2(setup_ini_source, setup_ini_dest)
                print(f"{Fore.BLUE}Copied setup.ini to project.{Style.RESET_ALL}")
            else:
                logging.warning(f"Setup.ini template not found: {setup_ini_source}")
        else:
            # If setup.ini exists, check and update the project name
            config = ConfigParser()
            config.read(setup_ini_dest, encoding='utf-8')
            
            if config.has_section('project') and config.has_option('project', 'name'):
                current_name = config.get('project', 'name')
                if current_name.lower() != 'greaterwms':
                    config.set('project', 'name', 'greaterwms')
                    with open(setup_ini_dest, "wt", encoding='utf-8') as configfile:
                        config.write(configfile)
                    print(f"{Fore.BLUE}Updated project name to 'greaterwms' in setup.ini{Style.RESET_ALL}")
            else:
                # If the section or option doesn't exist, create it
                if not config.has_section('project'):
                    config.add_section('project')
                config.set('project', 'name', 'greaterwms')
                with open(setup_ini_dest, "wt", encoding='utf-8') as configfile:
                    config.write(configfile)
                print(f"{Fore.BLUE}Added project name 'greaterwms' to setup.ini{Style.RESET_ALL}")

        # Create required directories
        for dir_name in ['logs', 'dbs']:
            dir_path = join(working_space, dir_name)
            if not exists(dir_path):
                makedirs(dir_path, exist_ok=True)

        welcome()
        
        return True
    except Exception as e:
        logging.error(f"Error during file creation: {str(e)}")
        return False