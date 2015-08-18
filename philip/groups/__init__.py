from philip.groups import get, delete, list, create
from philip.constants import parent_parser


def register_command(parser):
    subparsers = parser.add_subparsers()
    get.register_command(subparsers.add_parser('get', parents=[parent_parser], help='get group'))
    delete.register_command(subparsers.add_parser('delete', parents=[parent_parser], help='delete group'))
    list.register_command(subparsers.add_parser('list', parents=[parent_parser], help='list groups'))
    create.register_command(subparsers.add_parser('create', parents=[parent_parser], help='create group'))
