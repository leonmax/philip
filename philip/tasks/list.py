import json

import requests

from philip.constants import default_headers
from philip.outputter import print_json
from philip.config import load_server


def list_tasks(server, status=None):
    url = "%s/v2/tasks" % server.url
    params = {}
    if status:
        params['status'] = status

    r = requests.get(url, params=params, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def list_app_tasks(server, app_id):
    url = "%s/v2/apps/%s/tasks" % (server.url, app_id)

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    if args.app:
        result = list_app_tasks(server, args.app)
    else:
        result = list_tasks(server, args.status)
    print_json(result)


def register_command(parser):
    parser.add_argument("app", nargs="?", help="name of the app")
    parser.add_argument("-s", "--status", choices=["running", "staging"], help="name of the app")
    parser.set_defaults(func=run)
