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

    _marathon_config = namedtuple('Server', ['name', 'url', 'username', 'password'])
    _ecs_config = namedtuple('ECS_Config', ['cluster', 'aws_options'])

    def __init__(self):
        self.config = {}

    def _load_config(self, config_path=None):
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
        return self._marathon_config(provider, provider['url'], provider['username'], provider['password'])

    def _get_ecs_config(self, provider):
        return self._ecs_config(provider['cluster'], provider['aws_config'])

    def _get_config(self, profile, provider_name=None):
        provider = self._get_provider(profile)
        if provider_name:
            if provider_name != provider['provider_type']:  # TODO
                raise PhilipException('This profile does not support provider {}'.format(provider_name))
        if provider_name == 'marathon':
            return self._get_marathon_server(provider)
        if provider_name == 'ecs':
            return self._get_ecs_config(provider)

    def get(self, profile_names, config_path=None, provider_name=None):
        if not self.config or config_path:
            self._load_config(config_path)
        if 'profiles' not in self.config:
            raise PhilipException('You must specify at least one "profile" in your configuration')
        for profile in reversed(profile_names):
            profile = self._get_profile(profile)
            if profile:
                return self._get_config(profile, provider_name)
        raise PhilipException('Unable to load configuration')
