from philip.apps import update, get, list, version
from philip.parent import parent_parser

__author__ = 'leonmax'


def register_command(parser):
    subparsers = parser.add_subparsers()
    update.register_command(subparsers.add_parser('update', parents=[parent_parser], help='update an app'))
    get.register_command(subparsers.add_parser('get', parents=[parent_parser], help='get app'))
    list.register_command(subparsers.add_parser('list', parents=[parent_parser], help='list apps'))
    version.register_command(subparsers.add_parser('version', parents=[parent_parser], help='app versions'))
