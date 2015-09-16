# -*- coding: utf-8 -*-

from philip.models import Command
from philip.ecs.util import get_ecs, search_response, print_aws_response


class ListTasks(Command):

    name = 'list tasks'
    help = 'List Amazon ECS Tasks'
    description = 'List Amazon ECS Tasks'

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

        print_aws_response('Tasks', tasks_raw)


commands = [ListTasks]
description = 'Manage Amazon ECS Tasks'
