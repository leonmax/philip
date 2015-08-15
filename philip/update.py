#!/usr/bin/env python
import json

import requests

from philip.config import load_server
from philip.models import load_artifact


def deploy(server, artifact, dry_run=False):
    url = "%s/v2/apps/%s" % (server.url, artifact['id'])

    if dry_run:
        print(json.dumps({
            'artifact': artifact.conf,
            'server': server.__dict__
        }))
    else:
        r = requests.put(url, artifact.json, auth=(server.username, server.password))
        print(r.text)


def run(args):
    server = load_server(args.profiles, args.conffile)
    artifact = load_artifact(args.profiles, args.filename, args.tag)
    deploy(server, artifact, args.dry_run)


def register_parser(parser):
    parser.add_argument("-t", "--tag", type=str, help="docker tag")
    parser.add_argument("filename", nargs='?', default="Philipfile",
                        help="the message file Philip delivery to marathon")
    parser.set_defaults(func=run)
