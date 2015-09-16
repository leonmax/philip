import json
import yaml

from functools import reduce

from philip.config import Config
from philip.merger import merge
from philip.constants import parent_parser
from philip.exceptions import PhilipException


class Command:

    name = None
    help = 'No help is provided'
    description = 'No description provided'
    parents = [parent_parser]
    arguments = []
    calls = 0

    @staticmethod
    def config(arguments):
        return Config(arguments)

    @classmethod
    def add_argument(cls, *args, **kwargs):
        cls.arguments.append({'args': args, 'kwargs': kwargs})

    @classmethod
    def register(cls, subparsers):
        cmd = cls()
        parser = subparsers.add_parser(cls.name, description=cls.description, help=cls.help, parents=cls.parents)
        parser.set_defaults(func=cmd.execute)
        for arg in cls.arguments:
            parser.add_argument(*arg['args'], **arg['kwargs'])
        return cmd

    def execute(self, args):
        raise NotImplemented


class Artifact:
    def __init__(self, from_conf):
        self._conf = from_conf

    def __setitem__(self, key, value):
        last_dot = key.rfind('.')
        self.__getitem__(key[:last_dot])[key[last_dot + 1:]] = value

    def __getitem__(self, key):
        path = [] if not key else key.split(".")
        return reduce(lambda d, k: d[k], path, self._conf)

    @property
    def conf(self):
        return self._conf

    @property
    def json(self):
        return json.dumps(self._conf)

    def set_tag(self, tag=None):
        if tag:
            image = self["container.docker.image"]
            self["container.docker.image"] = "%s:%s" % (image.split(":")[0], tag)
        return self


def load_artifact(profile_names, filename, tag=None):
    try:
        with open(filename, 'r') as fp:
            artifact_conf = yaml.load(fp.read())

            if 'profiles' in artifact_conf:
                profiles_conf = artifact_conf['profiles']
                del artifact_conf['profiles']
                for profile in profile_names:
                    if profile in profiles_conf:
                        artifact_conf = merge(artifact_conf, profiles_conf[profile])

            return Artifact(artifact_conf).set_tag(tag)
    except IOError:
        raise PhilipException("{} WARNING: Job file %s not found" % filename)
