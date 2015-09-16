# -*- coding: utf-8 -*-

from philip.models import Command
from philip.util import dict_to_table
from philip.ecs.util import get_ecs, search_response


class ListInstances(Command):

    name = 'list'
    help = 'List Amazon ECS Instances'
    description = 'List Amazon ECS Instances'
    arguments = [
        {'args': ['-a', '--all'], 'kwargs': dict(
            default=False, help='Show all instance properties', action='store_true'
        )},
        {'args': ['-f', '--filter'], 'kwargs': dict(
            default=False, help='Show filtered instance properties. Separate values by comma, e.g. ec2InstanceId,status'
        )},
        {'args': ['-s', '--sort'], 'kwargs': dict(
            default=False, help='Sort by a specified key, e.g. "ec2InstanceId"'
        )}
    ]

    def execute(self, args):
        config = self.config(args).get()
        conn = get_ecs(config.aws_options)
        instance_ids = [
            x for x in search_response(
                'containerInstanceArns', conn.list_container_instances(cluster=config.cluster)
            )][0]

        instances_raw = [
            x for x in search_response(
                'containerInstances', conn.describe_container_instances(instance_ids)
            )][0]

        keys = ['status', 'ec2InstanceId', 'runningTasksCount']
        sort = 'ec2InstanceId'

        if args.filter:
            keys = args.filter.split(',')
        if args.all:
            keys = [x for x in instances_raw[0].keys()]
        if args.sort:
            sort = args.sort

        dict_to_table(instances_raw, keys=keys, sort=sort)


commands = [ListInstances]
description = 'Manage Amazon ECS Instances'
