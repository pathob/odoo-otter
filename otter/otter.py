import argparse
import sys

import otter.funcs as funcs
from otter.const import *
from otter.errors import *


try:
    from colorama import Fore, Back, Style, init
    init()
except ImportError:  # fallback so that the imported classes always exist
    class ColorFallback:
        __getattr__ = lambda self, name: ''
    Fore = Back = Style = ColorFallback()


def main(argv=None):
    try:
        main_internal(argv)
    except Error as e:
        print(e.message)
        sys.exit(1)
    except KeyboardInterrupt:
        print()  # print new line
        sys.exit(0)


def main_internal(argv):
    parser = argparse.ArgumentParser(description=OTTER_DESCRIPTION)
    parser.set_defaults(func=lambda x: parser.print_help())
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + OTTER_VERSION)
    commands = parser.add_subparsers(metavar='commands')

    subcommand = commands.add_parser('start', help="Start time tracking for a new task")
    subcommand.add_argument('--time', nargs="?", const="NOW", default="NOW")
    subcommand.set_defaults(func=funcs.start)

    subcommand = commands.add_parser('stop', help="Stop time tracking for current task")
    subcommand.add_argument('--time', nargs="?", const="NOW", default="NOW")
    subcommand.set_defaults(func=funcs.stop)

    subcommand = commands.add_parser('describe', help="Describe work for current task")
    subcommand.add_argument('description')
    subcommand.set_defaults(func=funcs.describe)

    subcommand = commands.add_parser('status', help="Get current time tracking status")
    subcommand.set_defaults(func=funcs.status)

    subcommand = commands.add_parser('show', help="Show tracked time for given date")
    subcommand.add_argument('--date', nargs="?", const="TODAY", default="TODAY")
    subcommand.set_defaults(func=funcs.show)

    subcommand = commands.add_parser('sync', help="Sync from and to Odoo")
    subcommand.add_argument('--date', nargs="?", const="YESTERDAY", default="YESTERDAY")
    subcommand.set_defaults(func=funcs.sync)

    subcommand = commands.add_parser('login', help="Login to Odoo")
    subcommand.add_argument('--url')
    subcommand.add_argument('--database')
    subcommand.add_argument('--username')
    subcommand.add_argument('--password')
    subcommand.set_defaults(func=funcs.login)

    subcommand = commands.add_parser('logout', help="Logout from Odoo")
    subcommand.set_defaults(func=funcs.logout)

    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except:
        pass

    args = parser.parse_args(args=argv)
    args.func(args)


if __name__ == '__main__':
    main()
