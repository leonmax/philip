import json

import requests

from philip.constants import default_headers
from philip.outputter import print_json
from philip.config import load_server


def stream_events(server):
    url = "%s/v2/events" % server.url
    headers = {
        "Accept": "text/event-stream",
        "Accept-Encoding": "gzip, deflate"
    }

    r = requests.get(url, auth=(server.username, server.password), headers=headers, stream=True)

    for line in r.iter_lines():
        # filter out keep-alive new lines
        if line:
            json_str = line.lstrip("data:").lstrip()
            print_json(json.loads(json_str))


def run(args):
    server = load_server(args.profiles, args.conffile)
    stream_events(server)


def register_command(parser):
    parser.set_defaults(func=run)

