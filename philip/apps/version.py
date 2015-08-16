import json

import requests

from philip.config import load_server
from philip.outputter import print_json


def list_app_versions(server, app_id):
    url = "%s/v2/apps/%s/versions" % (server.url, app_id)

    r = requests.get(url, auth=(server.username, server.password))
    return json.loads(r.text)


def get_app_version(server, app_id, version):
    url = "%s/v2/apps/%s/versions/%s" % (server.url, app_id, version)

    r = requests.get(url, auth=(server.username, server.password))
    return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    if args.version:
        result = get_app_version(server, args.app, args.version)
    else:
        result = list_app_versions(server, args.app)
    print_json(result)


def register_command(parser):
    parser.add_argument("app", type=str, help="app name")
    parser.add_argument("version", nargs="?", help="optional version")
    parser.set_defaults(func=run)
