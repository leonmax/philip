import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import load_server
from philip.outputter import print_json


def delete_group(server, app_id):
    url = "%s/v2/groups/%s" % (server.url, app_id)

    r = requests.delete(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = delete_group(server, args.app)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('delete', parents=[parent_parser], help='delete group')
    parser.set_defaults(func=run)

    parser.add_argument("group", type=str, help="name of the group")
