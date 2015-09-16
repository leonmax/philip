# -*- coding: utf-8 -*-

import requests

from philip.models import Command
from philip.constants import default_headers
from philip.marathon.util import print_response


class ListDeployments(Command):

    name = 'list'
    help = 'List Marathon Deployments'

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/deployments" % server.url
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


class DeleteDeployment(Command):

    name = 'delete'
    help = 'Delete a Marathon deployment'
    arguments = [
        {'args': ['deployment'], 'kwargs': dict(type=str, help='id of the deployment')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/deployments/%s" % (server.url, args.deployment)
        print_response(requests.delete(url, auth=(server.username, server.password), headers=default_headers))

commands = [ListDeployments, DeleteDeployment]
description = 'Marathon Deployments'
