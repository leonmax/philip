import argparse
from collections import namedtuple
from os import path

import yaml

from philip.exceptions import PhilipException

__author__ = 'leonmax'

DEFAULT_CONFIG_FILES = ['/etc/philip/config.json',
                        '/etc/philip/config.yaml',
                        '/etc/philip/config.yml',
                        '~/.config/philip/config.json',
                        '~/.config/philip/config.yaml',
                        '~/.config/philip/config.yml']

Profile = namedtuple('Profile', ['name', 'url', 'username', 'password'])

def load_profile(profile_name, conffile=None):
    if not conffile:
        for default_path in DEFAULT_CONFIG_FILES:
            if path.exists(path.expanduser(default_path)):
                conffile = path.expanduser(default_path)
                break
        else:
            raise PhilipException('no config file exists under ~/.config/philip')
    with open(conffile, 'r') as fp:
        config = yaml.load(fp.read())[profile_name]
        return Profile(profile_name, config['url'], config['username'], config['password'])