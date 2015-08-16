from philip.tasks import list
from philip.constants import parent_parser

__author__ = 'leonmax'


def register_command(parser):
    subparsers = parser.add_subparsers()
    list.register_command(subparsers.add_parser('list', parents=[parent_parser], help='list tasks'))
