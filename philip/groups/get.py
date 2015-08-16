import json

import requests

from philip.constants import default_headers
from philip.config import load_server
from philip.outputter import print_json


def get_group(server, group_id):
    url = "%s/v2/groups/%s" % (server.url, group_id)

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = get_group(server, args.group)
    print_json(result)


def register_command(parser):
    parser.add_argument("group", type=str, help="name of the group")
    parser.set_defaults(func=run)
