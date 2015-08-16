import json

import requests

from philip.config import load_server
from philip.outputter import print_json


def list_apps(server):
    url = "%s/v2/apps" % server.url

    r = requests.get(url, auth=(server.username, server.password))
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = list_apps(server)
    print_json(result)


def register_command(parser):
    parser.set_defaults(func=run)
