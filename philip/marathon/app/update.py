import json

import requests

from philip.constants import default_headers, parent_parser
from philip.config import Config
from philip.models import load_artifact
from philip.outputter import print_json

config = Config()


def update_app(server, artifact, dry_run=False, force=False):
    url = "%s/v2/apps/%s" % (server.url, artifact['id'])
    params = {}
    if force:
        params['force'] = True

    if dry_run:
        return {
            'artifact': artifact.conf,
            'server': server.__dict__
        }
    else:
        r = requests.put(url, artifact.json, params=params,
                         auth=(server.username, server.password), headers=default_headers)
        return json.loads(r.text) if r.text else {}


def run(args):
    server = config.get(args.profiles, args.conffile)
    artifact = load_artifact(args.profiles, args.message, args.tag)
    result = update_app(server, artifact, args.dry_run, args.force)
    print_json(result)


def register_command(subparsers):
    parser = subparsers.add_parser('update', parents=[parent_parser], help='update an app')
    parser.set_defaults(func=run)

    parser.add_argument("-f", "--force", action='store_true', help="name of the app")
    parser.add_argument("-t", "--tag", type=str, help="docker tag")
    parser.add_argument("--dry-run", action='store_true', help="dry run this command without really execute")
    parser.add_argument("-m", "--message", type=str, default="Philipfile",
                        help="the message file Philip delivery to marathon")
