import json

import requests

from philip.constants import default_headers, parent_parser
from philip.outputter import print_json
from philip.config import load_server


def kill_app_task(server, app_id, task_id, scale=False):
    url = "%s/v2/apps/%s/tasks/%s" % (server.url, app_id, task_id)
    params = {}
    if scale:
        params['scale'] = True

    r = requests.delete(url, params=params, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}

def kill_app_all_tasks(server, app_id, host=None, scale=False):
    url = "%s/v2/apps/%s/tasks" % (server.url, app_id)
    params = {}
    if scale:
        params['scale'] = True
    if host:
        params['host'] = host

    r = requests.delete(url, params=params, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    if args.task:
        result = kill_app_task(server, args.app, args.task, args.scale)
    else:
        result = kill_app_all_tasks(server, args.app, host=args.hostm, scale=args.scale)

    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('kill', parents=[parent_parser], help='kill tasks')
    parser.set_defaults(func=run)

    parser.add_argument("app", type=str, help="name of the app")
    parser.add_argument("task", nargs="?", help="name of the app")
    parser.add_argument("-H", "--host", type=str, help="Kill only those tasks running on host host. Default: None.")
    parser.add_argument("-s", "--scale", action="store_true", help="Scale the app down (i.e. decrement its instances "
                                                                   "setting by the number of tasks killed) after "
                                                                   "killing the specified tasks. Default: False.")
