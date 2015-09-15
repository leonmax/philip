import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import Config
from philip.outputter import print_json

config = Config()


def delete_app(server, app_id):
    url = "%s/v2/apps/%s" % (server.url, app_id)

    r = requests.delete(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = config.get(args.profiles, args.conffile)
    result = delete_app(server, args.app)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('delete', parents=[parent_parser], help='delete app')
    parser.set_defaults(func=run)

    parser.add_argument("app", type=str, help="name of the app")
