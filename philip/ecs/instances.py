# -*- coding: utf-8 -*-

from philip.models import Command
from philip.ecs.util import get_ecs, search_response, print_aws_response


class ListInstances(Command):

    name = 'list'
    help = 'List Amazon ECS Instances'

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

        print_aws_response('ECS_Instance', instances_raw)


commands = [ListInstances]
description = 'Manage Amazon ECS Instances'
