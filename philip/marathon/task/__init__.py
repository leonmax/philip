from philip.marathon.task import list
from philip.marathon.task import kill


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('task', help='api for tasks').add_subparsers()

    for sub_command in [list, kill]:
        sub_command.register_command(sub_subparsers)
