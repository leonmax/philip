from collections import namedtuple
from os import path

import yaml

from philip.exceptions import PhilipException


class Config:

    DEFAULT_CONFIG_FILES = ['/etc/philip/config.json',
                            '/etc/philip/config.yaml',
                            '/etc/philip/config.yml',
                            '~/.config/philip/config.json',
                            '~/.config/philip/config.yaml',
                            '~/.config/philip/config.yml']

    PROVIDERS = ['marathon', 'ecs']

    _marathon_server = namedtuple('Server', ['name', 'url', 'username', 'password'])

    def __init__(self):
        self.config = {}

    def _get_config(self, config_path=None):
        if not config_path:
            for default_path in self.DEFAULT_CONFIG_FILES:
                if path.exists(path.expanduser(default_path)):
                    config_path = path.expanduser(default_path)
                    break
        if not config_path:
            raise PhilipException('No configuration file present')
        with open(config_path, 'r') as fp:
            self.config = yaml.load(fp.read())

    def _get_profile(self, profile_name):
        if profile_name in self.config['profiles']:
            return self.config['profiles'][profile_name]

    def _get_provider(self, profile):
        if 'provider' not in profile:
            raise PhilipException('Profiles must specify a provider')
        if 'provider_type' not in profile['provider']:
            raise PhilipException('You must specify a provider_type')
        if profile['provider']['provider_type'] not in self.PROVIDERS:
            raise PhilipException('Unknown provider {}'.format(profile['provider']))
        return profile['provider']

    def _get_marathon_server(self, provider):
        print(provider)
        return self._marathon_server(provider, provider['url'], provider['username'], provider['password'])

    def _get_ecs_cluster(self, profile):
        pass

    def get(self, profile_names, config_path=None):
        if not self.config or config_path:
            self._get_config(config_path)
        if 'profiles' not in self.config:
            raise PhilipException('You must specify at least one "profile" in your configuration')
        for profile in reversed(profile_names):
            profile = self._get_profile(profile)
            if profile:
                provider = self._get_provider(profile)
                if provider['provider_type'] == 'marathon':
                    return self._get_marathon_server(provider)
        raise PhilipException('Unable to load configuration')


"""
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
"""