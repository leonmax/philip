# -*- coding: utf-8 -*-

import requests

from philip.models import Command
from philip.constants import default_headers
from philip.marathon.util import print_response


class ListTasks(Command):

    name = 'list'
    help = 'List Marathon Tasks'
    description = 'List Marathon Tasks'

    arguments = [
        {'args': ['app'], 'kwargs': dict(nargs="?", help="Name of the app")},
    ]

    @staticmethod
    def list_tasks(server, status=None):
        url = "%s/v2/tasks" % server.url
        params = {}
        if status:
            params['status'] = status

        return requests.get(url, params=params, auth=(server.username, server.password), headers=default_headers)

    @staticmethod
    def list_app_tasks(server, app_id):
        url = "%s/v2/apps/%s/tasks" % (server.url, app_id)
        return requests.get(url, auth=(server.username, server.password), headers=default_headers)

    def execute(self, args):
        server = self.config(args).get()
        if args.app:
            print_response(self.list_app_tasks(server, args.app))
        else:
            print_response(self.list_tasks(server, args.status))


class KillTasks(Command):

    name = 'kill'
    help = 'Kill Marathon Tasks'
    description = 'Kill Marathon Tasks'

    arguments = [
        {'args': ['app'], 'kwargs': dict(help='Name of the app')},
        {'args': ['task'], 'kwargs': dict(nargs='?', help='Name of the task')},
        {'args': ['-H', '--host'], 'kwargs': dict(help='Only kill tasks running on the specified host')},
        {'args': ['-S', '--scale'], 'kwargs': dict(action='store_true', help='Scale the app up or down')},
    ]

    @staticmethod
    def kill_app_task(server, app_id, task_id, scale=False):
        url = "%s/v2/apps/%s/tasks/%s" % (server.url, app_id, task_id)
        params = {}
        if scale:
            params['scale'] = True

        return requests.delete(url, params=params, auth=(server.username, server.password), headers=default_headers)

    @staticmethod
    def kill_app_all_tasks(server, app_id, host=None, scale=False):
        url = "%s/v2/apps/%s/tasks" % (server.url, app_id)
        params = {}
        if scale:
            params['scale'] = True
        if host:
            params['host'] = host

        return requests.delete(url, params=params, auth=(server.username, server.password), headers=default_headers)

    def execute(self, args):
        server = self.config(args).get()
        if args.task:
            print_response(self.kill_app_all_tasks(server, args.app, args.task, args.scale))
        else:
            print_response(self.kill_app_all_tasks(server, args.app, host=args.hostm, scale=args.scale))


commands = [KillTasks, ListTasks]
description = 'Manage Marathon Tasks'
