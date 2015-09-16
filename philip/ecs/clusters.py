# -*- coding: utf-8 -*-

from philip.models import Command
from philip.ecs.util import get_ecs, search_response, print_aws_response


class ListClusters(Command):

    name = 'list'
    help = 'List Amazon ECS Clusters'
    description = 'List Amazon ECS Clusters'

    def execute(self, args):
        config = self.config(args).get()
        conn = get_ecs(config.aws_options)

        cluster_ids = [
            x for x in search_response(
                'clusterArns', conn.list_clusters()
            )][0]

        clusters_raw = [
            x for x in search_response(
                'clusters', conn.describe_clusters(cluster_ids)
            )][0]

        print_aws_response('ECS_Cluster', clusters_raw)


commands = [ListClusters]
description = 'Amazon ECS Clusters'
