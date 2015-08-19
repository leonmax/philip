from philip.task import list, kill


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('task', help='api for tasks').add_subparsers()

    for sub_command in [list, kill]:
        sub_command.register_command(sub_subparsers)
