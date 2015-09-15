import json

import requests

from philip.constants import default_headers, parent_parser
from philip.outputter import print_json
from philip.config import Config

config = Config()


def info(server):
    url = "%s/v2/info" % server.url

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = config.get(args)
    result = info(server)

    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('info', parents=[parent_parser], help='Get info about the Marathon Instance')
    parser.set_defaults(func=run)
