import json
import requests

from philip.config import load_server
from philip.constants import parent_parser, default_headers


def usage(server):
    url = "%s/v2/apps?embed=apps.tasks" % server.url

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text)


def parse_usage(server, result):
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


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = usage(server)
    parse_usage(server, result)


def register_command(subparsers):
    parser = subparsers.add_parser('usage', parents=[parent_parser], help='Get info about the Marathon Instance')
    parser.set_defaults(func=run)
