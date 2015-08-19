import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import load_server
from philip.models import load_artifact
from philip.outputter import print_json


def create_group(server, artifact, dry_run=False):
    url = "%s/v2/groups" % server.url

    if dry_run:
        return {
            'artifact': artifact.conf,
            'server': server.__dict__
        }
    else:
        r = requests.post(url, artifact.json, auth=(server.username, server.password), headers=default_headers)
        return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    artifact = load_artifact(args.profiles, args.message)
    result = create_group(server, artifact, args.dry_run)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('create', parents=[parent_parser], help='create group')
    parser.set_defaults(func=run)

    parser.add_argument("--dry-run", action='store_true', help="dry run this command without really execute")
