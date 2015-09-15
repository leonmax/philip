from philip.marathon.group import get, delete, list, create


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('group', help='api for groups').add_subparsers()

    for sub_command in [create, get, delete, list]:
        sub_command.register_command(sub_subparsers)
