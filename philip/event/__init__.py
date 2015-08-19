from philip.event import stream


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('event', help='api for events').add_subparsers()

    for sub_command in [stream]:
        sub_command.register_command(sub_subparsers)
