from philip.marathon.deployment import delete, list


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('deployment', help='api for deployments').add_subparsers()

    for sub_command in [delete, list]:
        sub_command.register_command(sub_subparsers)
