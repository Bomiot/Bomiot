import sys
import os
import uvicorn
from bomiot import version
import argparse

optional_title = 'Optional arguments'


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super(CapitalisedHelpFormatter, self).__init__(prog,
                                                       indent_increment=2,
                                                       max_help_position=30,
                                                       width=200)
        self._action_max_length = 20

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:
                return ''

            # add the heading if the section was non-empty
            if self.heading is not argparse.SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                if self.heading == optional_title:
                    heading = '%*s%s:\n' % (current_indent, '', self.heading)
                else:
                    heading = '%*s%s:' % (current_indent, '', self.heading)
            else:
                heading = ''

            return join(['\n', heading, item_help])


parser = argparse.ArgumentParser(description='Bomiot %s - Distributed Crawler Management Framework' % version(),
                                 formatter_class=CapitalisedHelpFormatter, add_help=False)
parser._optionals.title = optional_title

parser.add_argument('-v', '--version', action='version',
                    version=version(), help='Get version of Bomiot')
parser.add_argument('-h', '--help', action='help',
                    help='Show this help message and exit')

subparsers = parser.add_subparsers(
    dest='command', title='Available commands', metavar='')

# new
parser_new = subparsers.add_parser(
    'new', help='Create APP for project')
parser_new.add_argument('folder', default='',
                         nargs='?', type=str, help='Create APP')

# project
parser_project = subparsers.add_parser(
    'project', help='Project workspace, default to bomiot')
parser_project.add_argument('folder', default='',
                         nargs='?', type=str, help='project workspace folder')

# plugins
parser_plugins = subparsers.add_parser(
    'plugins', help='Plugins workspace, default to bomiot')
parser_plugins.add_argument('folder', default='',
                         nargs='?', type=str, help='plugins workspace folder')

# deploy
parser_deploy = subparsers.add_parser(
    'deploy', help='Deploy project')
parser_deploy.add_argument('folder', default='',
                         nargs='?', type=str, help='deploy project')

# init
parser_init = subparsers.add_parser(
    'init', help='Init bomiot')
parser_init.add_argument('folder', default='',
                         nargs='?', type=str, help='Init Workingspace')

# init admin
parser_initadmin = subparsers.add_parser(
    'initadmin', help='Create default super user admin')

# init password
parser_initpwd = subparsers.add_parser(
    'initpwd', help='Init admin password')

# migrate
parser_migrate = subparsers.add_parser('migrate', help='Migrate database')

# makemigrations
parser_makemigrations = subparsers.add_parser(
    'makemigrations', help='Generate migrations for database')
parser_makemigrations.add_argument('appname', nargs='?', type=str, help='App name (e.g., xx or xxx.xx)')
parser_makemigrations.add_argument('--empty', action='store_true', help='Create an empty migration')
parser_makemigrations.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')

# loaddata
parser_loaddata = subparsers.add_parser(
    'loaddata', help='Load data from configs')
parser_loaddata.add_argument('source', type=str, help='Configs path')

# dumpdata
parser_dumpdata = subparsers.add_parser(
    'dumpdata', help='Dump data to configs')
parser_dumpdata.add_argument(
    'appname', default='core', nargs='?', type=str, help='Appname')

# marketplace
parser_marketplace = subparsers.add_parser(
    'market', help='Copy project from marketplace')
parser_marketplace.add_argument('folder', default='',
                         nargs='?', type=str, help='project marketplace folder')

# init auth keys
parser_keys = subparsers.add_parser(
    'keys', help='Init auth keys')

# run
parser_run = subparsers.add_parser(
    'run', help='Run server')
parser_run.add_argument("--host", "-b", type=str, default="127.0.0.1", help="Default Domin: 127.0.0.1")
parser_run.add_argument("--port", "-p", type=int, default=8000, help="Default Pore: 8000")
parser_run.add_argument("--workers", "-w", type=int, default=1, help="CPU Core")
parser_run.add_argument("--log-level", type=str, default="info", choices=["critical", "error", "warning", "info", "debug", "trace"], help="Log Level")
parser_run.add_argument("--uds", type=str, default=None, help="UNIX domain socket")
parser_run.add_argument("--ssl-keyfile", type=str, default=None, help="SSL Key")
parser_run.add_argument("--ssl-certfile", type=str, default=None, help="SSL PEM")
parser_run.add_argument("--proxy-headers", action="store_true", help="X-Forwarded-*Header")
parser_run.add_argument("--http", type=str, default="httptools", choices=["auto", "h11", "httptools"], help="HTTP")
parser_run.add_argument("--loop", type=str, default="auto", choices=["auto", "asyncio", "uvloop"], help="Asyncio Loop")
parser_run.add_argument("--app", type=str, default="bomiot.server.server.asgi:application", help="ASGI Application")

# show help info when no args
if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()


def cmd():
    """
    run from cmd
    :return:
    """
    args = parser.parse_args()
    command = args.command
    # project workspace for bomiot
    if command == 'project':
        from bomiot.cmd.project import project
        project(args.folder)
    # plugins workspace for bomiot
    elif command == 'plugins':
        from bomiot.cmd.plugins import plugins
        plugins(args.folder)
    # deploy project
    elif command == 'deploy':
        from bomiot.cmd.deploy import deploy
        deploy(args.folder)
    # init bomiot
    elif command == 'init':
        from bomiot.cmd.init import create_file
        create_file(args.folder)
    # init admin
    elif command == 'initadmin':
        from bomiot.cmd.initadmin import init_admin
        init_admin()
    # init admin
    elif command == 'initpwd':
        from bomiot.cmd.initpwd import init_password
        init_password()
    # create app
    elif command == 'new':
        from bomiot.cmd.createapp import new_app
        new_app(args.folder)
    # marketplace
    elif command == 'market':
        from bomiot.cmd.market import copy_project
        copy_project(args.folder)
    # init auth keys
    elif command == 'keys':
        from bomiot.cmd.create_key import auth_key_refresh
        auth_key_refresh()
    # makemigrations
    elif command == 'makemigrations':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
        os.environ.setdefault('RUN_MAIN', 'true')
        import django
        django.setup()
        from django.core.management import call_command
        from django.conf import settings
        from django.apps import apps
        appname = args.appname
        empty = args.empty
        dry_run = args.dry_run
        cmd_args = ['makemigrations']
        if appname:
            if '.' in appname:
                found_app_label = None
                for app_config in apps.get_app_configs():
                    if app_config.name == appname:
                        found_app_label = app_config.label
                        break
                if found_app_label:
                    cmd_args.append(found_app_label)
                else:
                    return
            else:
                found_app = None
                for app_config in apps.get_app_configs():
                    if app_config.label == appname or app_config.name.endswith('.' + appname):
                        found_app = app_config.label
                        break
                if found_app:
                    cmd_args.append(found_app)
                else:
                    return
        else:
            apps_with_models = []
            for app_config in apps.get_app_configs():
                try:
                    if app_config.models_module:
                        models = apps.get_app_config(app_config.label).get_models()
                        if models:
                            apps_with_models.append(app_config.label)
                except Exception:
                    continue
            if apps_with_models:
                cmd_args.extend(apps_with_models)
            else:
                return
        if empty:
            cmd_args.append('--empty')
        if dry_run:
            cmd_args.append('--dry-run')
        try:
            call_command(*cmd_args)
        except Exception as e:
            print(f"Error creating migrations: {e}")
    # migrate
    elif command == 'migrate':
        from bomiot.cmd.migrate import migrate
        migrate()
    # run server
    elif command == 'run':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
        os.environ.setdefault('RUN_MAIN', 'true')
        uvicorn.run(
            args.app,
            host=args.host,
            port=args.port,
            workers=args.workers,
            log_level=args.log_level,
            uds=args.uds,
            ssl_keyfile=args.ssl_keyfile,
            ssl_certfile=args.ssl_certfile,
            proxy_headers=args.proxy_headers,
            http=args.http,
            loop=args.loop
        )

# for console debugger
if __name__ == '__main__':
    cmd()
