from philip.apps import update, get, restart, delete, list, version
from philip.constants import parent_parser


def register_command(parser):
    subparsers = parser.add_subparsers()
    update.register_command(subparsers.add_parser('update', parents=[parent_parser], help='update an app'))
    get.register_command(subparsers.add_parser('get', parents=[parent_parser], help='get app'))
    restart.register_command(subparsers.add_parser('restart', parents=[parent_parser], help='restart app'))
    delete.register_command(subparsers.add_parser('delete', parents=[parent_parser], help='delete app'))
    list.register_command(subparsers.add_parser('list', parents=[parent_parser], help='list apps'))
    version.register_command(subparsers.add_parser('version', parents=[parent_parser], help='app versions'))
