# -*- coding: utf-8 -*-

from collections import namedtuple

from boto import connect_ec2containerservice


def get_ecs(aws_options):
    return connect_ec2containerservice(**aws_options)


def search_response(term, container):
    if term in container:
        yield container[term]
    for key in container:
        if isinstance(container[key], dict):
            for result in search_response(term, container[key]):
                yield result


def aws_response_to_tuple(name, response):
    t = namedtuple(name, [x for x in response[0].keys()])
    responses = []
    for r in response:
        responses.append(t(*[x for x in r.values()]))
    return responses


def print_aws_response(name, response):
    responses = aws_response_to_tuple(name, response)
    for index, response in enumerate(responses):
        print('{} {}'.format(index, response))
