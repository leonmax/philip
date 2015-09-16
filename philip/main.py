# -*- coding: utf-8 -*-
# import argcomplete

from philip.constants import HelpOnErrorArgumentParser
from philip import marathon, ecs


def load_modules(subparsers, modules):
    for module in modules:
        package_name = module.__name__.split('.')[-1]
        package_parser = subparsers.add_parser(package_name, help=module.description).add_subparsers()
        for cmd_module in module.command_modules:
            module_name = cmd_module.__name__.split('.')[-1]
            module_parser = package_parser.add_parser(module_name, help=cmd_module.description).add_subparsers()
            for command in cmd_module.commands:
                command.register(module_parser)


def main():
    parser = HelpOnErrorArgumentParser(
        prog='Philip',
        description='Philip is a service agnostic command line tool for deploying Docker containers.'
    )

    subparsers = parser.add_subparsers(parser_class=HelpOnErrorArgumentParser, help='sub-command help', dest='parser')
    subparsers.required = True  # Partial fix for Python 3 bug: http://bugs.python.org/issue16308

    load_modules(subparsers, [marathon, ecs])

    # argcomplete.autocomplete(parser) # TODO: This doesn't work?
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
