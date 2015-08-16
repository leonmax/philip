import json

import requests

from philip.constants import default_headers
from philip.config import load_server
from philip.models import load_artifact
from philip.outputter import print_json


def update_app(server, artifact, dry_run=False):
    url = "%s/v2/apps/%s" % (server.url, artifact['id'])

    if dry_run:
        return {
            'artifact': artifact.conf,
            'server': server.__dict__
        }
    else:
        r = requests.put(url, artifact.json, auth=(server.username, server.password), headers=default_headers)
        return json.loads(r.text) if r.text else {}


def run(args):
    server = load_server(args.profiles, args.conffile)
    artifact = load_artifact(args.profiles, args.message, args.tag)
    result = update_app(server, artifact, args.dry_run)
    print_json(result)


def register_command(parser):
    parser.add_argument("-t", "--tag", type=str, help="docker tag")
    parser.add_argument("--dry-run", action='store_true', help="dry run this command without really execute")
    parser.set_defaults(func=run)
