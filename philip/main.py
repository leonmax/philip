__author__ = 'leonmax'

import argparse

import apps
import tasks


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    apps.register_command(subparsers.add_parser('app', help='api for apps'))
    tasks.register_command(subparsers.add_parser('task', help='api for tasks'))

    args = parser.parse_args()
    args.func(args)
