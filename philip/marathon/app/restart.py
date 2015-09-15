import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import Config
from philip.outputter import print_json

config = Config()


def restart_app(server, app_id, force=False):
    url = "%s/v2/apps/%s/restart" % (server.url, app_id)
    params = {}
    if force:
        params['force'] = True

    r = requests.post(url, params=params, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = config.get(args)
    result = restart_app(server, args.app, args.force)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('restart', parents=[parent_parser], help='restart app')
    parser.set_defaults(func=run)

    parser.add_argument("app", type=str, help="name of the app")
    parser.add_argument("-f", "--force", action='store_true', help="name of the app")
