import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import Config
from philip.outputter import print_json

config = Config()


def get_group(server, group_id):
    url = "%s/v2/groups/%s" % (server.url, group_id)

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = config.get(args)
    result = get_group(server, args.group)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('get', parents=[parent_parser], help='get group')
    parser.set_defaults(func=run)

    parser.add_argument("group", type=str, help="name of the group")
