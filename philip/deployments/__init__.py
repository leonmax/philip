from philip.deployments import list, delete
from philip.constants import parent_parser

__author__ = 'leonmax'


def register_command(parser):
    subparsers = parser.add_subparsers()
    list.register_command(subparsers.add_parser('list', parents=[parent_parser], help='list deployments'))
    delete.register_command(subparsers.add_parser('delete', parents=[parent_parser], help='delete deployment'))
