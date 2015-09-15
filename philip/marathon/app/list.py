import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import Config
from philip.outputter import print_json

config = Config()


def list_apps(server, cmd="", embed=None):
    url = "%s/v2/apps" % server.url
    params = {}
    if cmd:
        params['cmd'] = True
    if embed:
        params['embed'] = True

    r = requests.get(url, auth=(server.username, server.password), headers=default_headers)
    return json.loads(r.text) if r.text else {}


def run(args):
    server = config.get(args.profiles, args.conffile)
    result = list_apps(server)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('list', parents=[parent_parser], help='list apps')
    parser.set_defaults(func=run)

    parser.add_argument("--cmd", type=str, default="",
                        help='Filter apps to only those whose commands contain cmd. Default: "."')
    parser.add_argument("--embed", choices=["apps.tasks", "apps.failures"], default=None,
                        help='Embeds nested resources that match the supplied path. Default: none. Possible values:\n'
                             '"apps.tasks".    Apps tasks are not embedded in the response by default.\n'
                             '"apps.failures". Apps last failures are not embedded in the response by default.')
