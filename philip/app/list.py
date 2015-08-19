import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import load_server
from philip.outputter import print_json


def list_apps(server):
    url = "%s/v2/apps" % server.url

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = list_apps(server)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('list', parents=[parent_parser], help='list apps')
    parser.set_defaults(func=run)

    parser.add_argument("app", type=str, help="name of the app")
