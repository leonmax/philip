import argcomplete

from constants import HelpOnErrorArgumentParser
import app
import task
import group
import deployment
import server
import event


def main():
    parser = HelpOnErrorArgumentParser()
    subparsers = parser.add_subparsers(parser_class=HelpOnErrorArgumentParser, help='sub-command help')

    for sub_command in [app, task, group, deployment, server, event]:
        sub_command.register_command(subparsers)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)
