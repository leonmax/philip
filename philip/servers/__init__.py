from philip.servers import info, leader
from philip.constants import parent_parser

__author__ = 'leonmax'


def register_command(parser):
    subparsers = parser.add_subparsers()
    info.register_command(subparsers.add_parser(
        'info', parents=[parent_parser], help='Get info about the Marathon Instance'))
    leader.register_command(subparsers.add_parser(
        'leader', parents=[parent_parser],
        help='Returns the current leader. If no leader exists, Marathon will respond with a 404 error.'))
