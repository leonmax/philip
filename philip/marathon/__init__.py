# -*- coding: utf-8 -*-

from philip.marathon import app, deployment, event, group, server, task


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('marathon', help='marathon deployment').add_subparsers()

    for sub_command in [app, deployment, event, group, server, task]:
        sub_command.register_command(sub_subparsers)