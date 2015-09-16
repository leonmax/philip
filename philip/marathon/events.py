# -*- coding: utf-8 -*-

import requests

from philip.models import Command


class StreamEvents(Command):

    name = 'stream'
    help = 'Interact the with Marathon EventBus'

    def execute(self, args):
        server = self.config(args).get()

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


commands = [StreamEvents]
description = 'Marathon Event Bus'
