from philip.app import update, get, restart, delete, list, version


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('app', help='api for apps').add_subparsers()

    for sub_command in [update, get, restart, delete, list, version]:
        sub_command.register_command(sub_subparsers)
