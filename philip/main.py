import argparse

import apps
import tasks
import groups
import deployments


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    apps.register_command(subparsers.add_parser('app', help='api for apps'))
    tasks.register_command(subparsers.add_parser('task', help='api for tasks'))
    groups.register_command(subparsers.add_parser('group', help='api for groups'))
    deployments.register_command(subparsers.add_parser('deployment', help='api for deployments'))

    args = parser.parse_args()
    args.func(args)
