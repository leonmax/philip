#!/usr/bin/env python

import yaml
import json
import requests
import copy
from os import path
from collections import namedtuple

DEFAULT_CONFIG_FILES = ['/etc/philip/config.json',
                        '/etc/philip/config.yaml',
                        '/etc/philip/config.yml',
                        '~/.config/philip/config.json',
                        '~/.config/philip/config.yaml',
                        '~/.config/philip/config.yml']

Profile = namedtuple('Profile', ['name', 'url', 'username', 'password'])

class Artifact:
    def __init__(self, from_conf):
        self._conf = from_conf

    def __setitem__(self, key, value):
        last_dot = key.rfind('.')
        self.__getitem__(key[:last_dot])[key[last_dot+1:]] = value

    def __getitem__(self, key):
        path = [] if not key else key.split(".")
        return reduce(lambda d,k: d[k], path, self._conf)

    @property
    def json(self):
        return json.dumps(self._conf)

    def set_tag(self, tag=None):
        if tag:
            image = self["container.docker.image"]
            self["container.docker.image"] = "%s:%s" % (image.split(":")[0], tag)
        return self


def deploy(profile, artifact, dry_run=False):
    url = "%s/v2/apps/%s" % (profile.url, artifact['id'])

    if dry_run:
        print(json.dumps({
            'artifact': artifact._conf,
            'profile': profile.__dict__
        }))
    else:
        r = requests.put(url, artifact.json, auth=(profile.username, profile.password))
        print(r.text)


def merge(d1, d2):
    # completely replace d1 with d2
    if d2 is None:
        return copy.deepcopy(d1)
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        return copy.deepcopy(d2)
    result = copy.deepcopy(d1)
    for key in d2:
        if key in result:
            result[key] = merge(result[key], d2[key])
        elif d2[key] is not None:
            result[key] = d2[key]
    return result


def load_artifact(profile, filename, tag=None):
    with open(filename, 'r') as fp:
        artifact_conf = yaml.load(fp.read())

        if 'profiles' in artifact_conf:
            profiles_conf = artifact_conf['profiles']
            del artifact_conf['profiles']
            if profile.name in profiles_conf:
                artifact_conf = merge(artifact_conf, profiles_conf[profile.name])

        return Artifact(artifact_conf).set_tag(tag)


def load_profile(profile_name, conffile=None):
    if not conffile:
        for default_path in DEFAULT_CONFIG_FILES:
            if path.exists(path.expanduser(default_path)):
                conffile = path.expanduser(default_path)
                break
        else:
            # change exception to a customized one
            raise Exception('no config file exists under ~/.config/philip')
    with open(conffile, 'r') as fp:
        config = yaml.load(fp.read())[profile_name]
        return Profile(profile_name, config['url'], config['username'], config['password'])


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, default="Philipfile", help="config filename")
    parser.add_argument("--dry-run", action='store_true', help="dry run this deploy without really execute")
    parser.add_argument("-p", "--profile", type=str, default="stage", help="profile to run")
    parser.add_argument("-t", "--tag", type=str, help="docker tag")
    parser.add_argument("-c", "--conffile", type=str, default=None,
            help="config file of the deployment script, by default locates at ~/.config/philip/config.json")

    args = parser.parse_args()

    profile = load_profile(args.profile, args.conffile)
    artifact = load_artifact(profile, args.filename, args.tag)
    deploy(profile, artifact, args.dry_run)
    return 0

