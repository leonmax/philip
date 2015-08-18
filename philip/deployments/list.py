import json

import requests

from philip.constants import default_headers
from philip.outputter import print_json
from philip.config import load_server


def list_deployments(server):
    url = "%s/v2/deployments" % server.url

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = list_deployments(server)
    print_json(result)


def register_command(parser):
    parser.set_defaults(func=run)
