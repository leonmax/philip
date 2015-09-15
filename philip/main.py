import argcomplete

from philip.constants import HelpOnErrorArgumentParser
from philip import marathon


def main():
    parser = HelpOnErrorArgumentParser(
        prog='Philip',
        description='Philip is a service agnostic command line tool for deploying Docker containers.'
    )

    subparsers = parser.add_subparsers(parser_class=HelpOnErrorArgumentParser, help='sub-command help', dest='parser')
    subparsers.required = True  # Partial fix for Python 3 bug: http://bugs.python.org/issue16308

    for sub_command in [marathon]:
        sub_command.register_command(subparsers)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
