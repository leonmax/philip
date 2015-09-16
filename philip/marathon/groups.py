# -*- coding: utf-8 -*-

import requests

from philip.models import Command, load_artifact
from philip.constants import default_headers
from philip.marathon.util import print_response


class CreateGroup(Command):

    name = 'create'
    help = 'Create a Marathon Group'

    arguments = [
        {'args': ['-m', '--message'], 'kwargs': dict(default='Philipfile', help='Philipfile')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        artifact = load_artifact(args.profiles, args.message)
        if args.dry_run:
            print_response({'artifact': artifact.conf, 'server': server.__dict__})
        else:
            url = "%s/v2/groups" % server.url
            print_response(requests.post(url, artifact.json, auth=(server.username, server.password),
                                         headers=default_headers))


class DeleteGroup(Command):

    name = 'delete'
    help = 'Delete a Marathon Group'
    description = 'Delete a group'
    arguments = [
        {'args': ['group'], 'kwargs': dict(help='Name of the group')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/groups/%s" % (server.url, args.app)
        print_response(requests.delete(url, auth=(server.username, server.password), headers=default_headers))


class GetGroup(Command):

    name = 'get'
    help = 'Get a Marathon Group'
    description = 'Get a group'

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/groups/%s" % (server.url, args.group)
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


class ListGroup(Command):

    name = 'list'
    help = 'List a Marathon group'
    description = 'List a group'

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/groups" % server.url
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


commands = [CreateGroup, DeleteGroup, GetGroup, ListGroup]
description = 'Interact with Marathon Groups'
