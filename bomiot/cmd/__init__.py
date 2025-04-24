import sys
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
parser_project = subparsers.add_parser(
    'new', help='Create APP for project')
parser_project.add_argument('folder', default='',
                         nargs='?', type=str, help='Create APP')

# project
parser_project = subparsers.add_parser(
    'project', help='project workspace, default to bomiot')
parser_project.add_argument('folder', default='',
                         nargs='?', type=str, help='project workspace folder')

# plugins
parser_plugins = subparsers.add_parser(
    'plugins', help='plugins workspace, default to bomiot')
parser_plugins.add_argument('folder', default='',
                         nargs='?', type=str, help='plugins workspace folder')

# deploy
parser_deploy = subparsers.add_parser(
    'deploy', help='deploy project')
parser_deploy.add_argument('folder', default='',
                         nargs='?', type=str, help='deploy project')

# init
parser_init = subparsers.add_parser(
    'init', help='Init bomiot')
parser_init.add_argument('folder', default='',
                         nargs='?', type=str, help='Init Bomiot')

# init admin
parser_initadmin = subparsers.add_parser(
    'initadmin', help='Create default super user admin')

# migrate
parser_migrate = subparsers.add_parser('migrate', help='Migrate database')

# makemigrations
parser_makemigrations = subparsers.add_parser(
    'makemigrations', help='Generate migrations for database')

# loaddata
parser_loaddata = subparsers.add_parser(
    'loaddata', help='Load data from configs')
parser_loaddata.add_argument('source', type=str, help='Configs path')

# dumpdata
parser_dumpdata = subparsers.add_parser(
    'dumpdata', help='Dump data to configs')
parser_dumpdata.add_argument(
    'appname', default='core', nargs='?', type=str, help='Appname')

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
    # create app
    elif command == 'new':
        from bomiot.cmd.createapp import new_app
        new_app(args.folder)
    else:
        from bomiot.server.manage import manage
        manage()


# for console debugger
if __name__ == '__main__':
    cmd()
