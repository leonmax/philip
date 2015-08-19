import json

import requests

from philip.constants import default_headers, parent_parser
from philip.outputter import print_json
from philip.config import load_server


def delete_deployment(server, deployment_id):
    url = "%s/v2/deployments/%s" % (server.url, deployment_id)

    r = requests.delete(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    result = delete_deployment(server, args.deployment)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('delete', parents=[parent_parser], help='delete deployment')
    parser.set_defaults(func=run)

    parser.add_argument("deployment", type=str, help="id of the deployment")
