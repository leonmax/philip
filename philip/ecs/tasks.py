# -*- coding: utf-8 -*-

from philip.models import Command
from philip.util import dict_to_table
from philip.ecs.util import get_ecs, search_response


class ListTasks(Command):

    name = 'list'
    help = 'List Amazon ECS Tasks'
    description = 'List Amazon ECS Tasks'
    arguments = [
        {'args': ['-C', '--containers'], 'kwargs': dict(
            default=False, action='store_true', help='Show containers associated with tasks')}
    ]

    def execute(self, args):
        config = self.config(args).get()
        conn = get_ecs(config.aws_options)

        task_ids = [
            x for x in search_response(
                'taskArns', conn.list_tasks(cluster=config.cluster)
            )][0]

        tasks_raw = [
            x for x in search_response(
                'tasks', conn.describe_tasks(task_ids)
            )][0]

        keys = ['taskArn', 'lastStatus', 'desiredStatus']
        container_keys = ['containerArn', 'name', 'lastStatus', 'reason', 'exitCode']

        dict_to_table(tasks_raw, keys=keys, sort='taskArn')

        if args.containers:
            containers = []
            for task in tasks_raw:
                containers.extend([x for x in task['containers']])
            dict_to_table(containers, keys=container_keys, sort='name')

commands = [ListTasks]
description = 'Manage Amazon ECS Tasks'
