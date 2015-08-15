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

Server = namedtuple('Server', ['name', 'url', 'username', 'password'])

def load_server(profile_names, conffile=None):
    if not conffile:
        for default_path in DEFAULT_CONFIG_FILES:
            if path.exists(path.expanduser(default_path)):
                conffile = path.expanduser(default_path)
                break
        else:
            raise PhilipException('no config file exists under /etc/philip or ~/.config/philip')
    with open(conffile, 'r') as fp:
        config = yaml.load(fp.read())
        for profile in reversed(profile_names):
            if profile in config:
                server_config = config[profile]
                return Server(profile, server_config['url'], server_config['username'], server_config['password'])