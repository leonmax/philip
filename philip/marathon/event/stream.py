import requests

from philip.constants import parent_parser
from philip.config import Config

config = Config()


def stream_events(server):
    url = "%s/v2/events" % server.url
    headers = {
        "Accept": "text/event-stream",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        r = requests.get(url, auth=(server.username, server.password), headers=headers, stream=True)

        for line in r.iter_lines():
            # filter out keep-alive new lines
            if line:
                data_str = line.lstrip("data:").lstrip()
                print(data_str)
    except KeyboardInterrupt:
        # If the user hits Ctrl+C, we don't want to print a traceback to the user.
        pass


def run(args):
    server = config.get(args)
    stream_events(server)


def register_command(subparsers):
    parser = subparsers.add_parser('stream', parents=[parent_parser], help='Attach to the marathon event stream.')
    parser.set_defaults(func=run)

