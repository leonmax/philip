# -*- coding: utf-8 -*-

import requests

from philip.models import Command
from philip.constants import default_headers
from philip.marathon.util import print_response


class ServerInfo(Command):

    name = 'info'
    help = 'Marathon Server Info'
    description = 'Marathon Server Info'

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/info" % server.url
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


class Leader(Command):

    name = 'leader'
    help = 'Return the current Marathon leader'
    description = 'Return the current Marathon leader'

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/leader" % server.url
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


class Usage(Command):

    name = 'usage'
    help = 'View Marathon Server Usage'
    description = 'View Marathon Server Usage'

    def parse_usage(self, server, result):
        apps = [x for x in result['apps']]
        cpu_usage = 0
        mem_usage = 0
        disk_usage = 0
        task_count = 0
        hosts = list()
        for app in apps:
            tasks = None
            if 'tasks' in app:
                tasks = app['tasks']
                task_count += len(tasks)
            if tasks:
                hosts.extend([x['host'] for x in tasks])
                mem_usage += app['mem'] * len(app['tasks'])
                cpu_usage += app['cpus'] * len(app['tasks'])
                disk_usage += app['disk'] * len(app['tasks'])
        hosts = set(hosts)
        print(' ######### Marathon Cluster Status - {} ########## '.format(server.url))
        print('Hosts: \n{}'.format('\n'.join(hosts)))
        print('Apps running: {}'.format(len(apps)))
        print('Tasks running: {}'.format(task_count))
        print('Memory Usage: {}'.format(mem_usage))
        print('CPU Usage: {}'.format(cpu_usage))
        print('Disk Usage: {}'.format(disk_usage))

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/apps?embed=apps.tasks" % server.url
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))

commands = [Usage, Leader, ServerInfo]
description = 'Marathon Server Usage'
