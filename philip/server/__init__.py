from philip.server import info, leader


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('server', help='api for servers').add_subparsers()

    for sub_command in [info, leader]:
        sub_command.register_command(sub_subparsers)
