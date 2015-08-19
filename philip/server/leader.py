import json

import requests

from philip.constants import default_headers, parent_parser
from philip.outputter import print_json
from philip.config import load_server


def leader(server):
    url = "%s/v2/leader" % server.url

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = leader(server)

    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('leader', parents=[parent_parser],
                                   help='Returns the current leader. If no leader exists, '
                                        'Marathon will respond with a 404 error.')
    parser.set_defaults(func=run)
