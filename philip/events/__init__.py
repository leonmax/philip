from philip.events import stream
from philip.constants import parent_parser

__author__ = 'leonmax'


def register_command(parser):
    subparsers = parser.add_subparsers()
    stream.register_command(subparsers.add_parser('stream', parents=[parent_parser],
                                                  help='Attach to the marathon event stream.'))
