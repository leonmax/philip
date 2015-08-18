import argparse

import apps
import tasks
import groups
import deployments
import servers
import events


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    apps.register_command(subparsers.add_parser('app', help='api for apps'))
    tasks.register_command(subparsers.add_parser('task', help='api for tasks'))
    groups.register_command(subparsers.add_parser('group', help='api for groups'))
    deployments.register_command(subparsers.add_parser('deployment', help='api for deployments'))
    servers.register_command(subparsers.add_parser('server', help='api for server info'))
    events.register_command(subparsers.add_parser('event', help='api for server info'))

    args = parser.parse_args()
    args.func(args)
