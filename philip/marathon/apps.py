# -*- coding: utf-8 -*-

import requests

from philip.models import Command, load_artifact
from philip.constants import default_headers
from philip.marathon.util import print_response


class CreateApp(Command):

    name = 'create'
    help = 'Create Applications'
    description = 'Create Apps'
    arguments = [
        {'args': ['--dry-run'], 'kwargs': dict(action='store_true', help='Test the command output')},
        {'args': ['-m', '--message'], 'kwargs': dict(type=str, default='Philipfile')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        artifact = load_artifact(args.profiles, args.message)
        if args.dry_run:
            print_response({'artifact': artifact.conf, 'server': server.__dict__})
        else:
            url = "%s/v2/apps" % server.url
            print_response(requests.post(url, artifact.json, auth=(server.username, server.password),
                                         headers=default_headers))


class DeleteApp(Command):

    name = 'delete'
    help = 'Delete Applications'
    description = 'Delete Applications'
    arguments = [
        {'args': ['all'], 'kwargs': dict(help='Name of the application')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/apps/%s" % (server.url, args.app)
        print_response(requests.delete(url, auth=(server.username, server.password), headers=default_headers))


class GetApp(Command):

    name = 'get'
    help = 'Get Marathon Applications'
    description = 'Get a Marathon app'
    arguments = [
        {'args': ['app'], 'kwargs': dict(help='Name of the application')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/apps/%s" % (server.url, args.app)
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


class ListApps(Command):
    name = 'list'
    help = 'List Marathon Applications'
    description = 'List Marathon Applications'
    arguments = [
        {'args': ['--cmd'], 'kwargs': dict(default="", help='Filter apps with a cmd')},
        {'args': ['--embed'], 'kwargs': dict(choices=['app.tasks', 'app.failures'])}
    ]

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/apps" % server.url
        params = {}
        if args.cmd:
            params['cmd'] = True
        if args.embed:
            params['embed'] = True
        print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


class RestartApp(Command):
    name = 'restart'
    help = 'Restart Marathon Applications'
    description = 'Restart Marathon Application'
    arguments = [
        {'args': ['app'], 'kwargs': dict(help='Name of the app')},
        {'args': ['-f', '--force'], 'kwargs': dict(dest='force_restart', action='store_true', help='Name of the app')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        url = "%s/v2/apps/%s/restart" % (server.url, args.app)
        params = {}
        if args.force:
            params['force'] = True
        print_response(
            requests.post(url, params=params, auth=(server.username, server.password), headers=default_headers)
        )


class UpdateApp(Command):
    name = 'update'
    help = 'Update Marathon Applications'
    description = 'Update Marathon Application'
    arguments = [
        {'args': ['-f', '--force'], 'kwargs': dict(action='store_true', help='Name of the app')},
        {'args': ['-t', '--tag'], 'kwargs': dict(help='docker tag')},
        {'args': ['--dry-run'], 'kwargs': dict(action='store_true', help='Test the command without execution')},
        {'args': ['-m', '--message'], 'kwargs': dict(default='Philipfile', help='Specify the Philipfile')}
    ]

    def execute(self, args):
        server = self.config(args).get()
        artifact = load_artifact(args.profiles, args.message, args.tag)
        url = "%s/v2/apps/%s" % (server.url, artifact['id'])
        params = {}
        if args.force:
            params['force'] = True
        if args.dry_run:
            print_response({'artifact': artifact.conf, 'server': server.__dict__})
        else:
            print_response(
                requests.put(url, artifact.json, params=params, auth=(
                    server.username, server.password), headers=default_headers)
            )


class Version(Command):

    name = 'version'
    help = 'Get an Application Version'
    description = 'Get an Application Version'
    arguments = [
        {
            'args': ['app'],
            'kwargs': dict(type=str, help='Optional Version')
        }
    ]

    def execute(self, args):
        server = self.config(args).get()
        if args.version:
            url = "%s/v2/apps/%s/versions" % (server.url, args.app)
            print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))

        else:
            url = "%s/v2/apps/%s/versions/%s" % (server.url, args.app, args.version)
            print_response(requests.get(url, auth=(server.username, server.password), headers=default_headers))


commands = [CreateApp, DeleteApp, ListApps, GetApp, UpdateApp, Version]
description = 'Marathon Applications'
