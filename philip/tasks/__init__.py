from philip.tasks import list, kill
from philip.constants import parent_parser

__author__ = 'leonmax'


def register_command(parser):
    subparsers = parser.add_subparsers()
    list.register_command(subparsers.add_parser('list', parents=[parent_parser], help='list tasks'))
    kill.register_command(subparsers.add_parser('kill', parents=[parent_parser], help='kill tasks'))
