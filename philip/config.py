from collections import namedtuple
from os import path

import yaml

from philip.exceptions import PhilipException

MarathonServer = namedtuple('MarathonServer', ['name', 'url', 'username', 'password'])
ECSConfig = namedtuple('ECSConfig', ['cluster', 'aws_options'])


class Config:

    DEFAULT_CONFIG_FILES = ['/etc/philip/config.json',
                            '/etc/philip/config.yaml',
                            '/etc/philip/config.yml',
                            '~/.config/philip/config.json',
                            '~/.config/philip/config.yaml',
                            '~/.config/philip/config.yml']

    PROVIDERS = ['marathon', 'ecs']

    def __init__(self, arguments):
        self.arguments = arguments
        self.profile_names = arguments.profiles
        self.config = self._load_config(arguments.conffile)

    def _load_config(self, config_path=None):
        if not config_path:
            for default_path in self.DEFAULT_CONFIG_FILES:
                if path.exists(path.expanduser(default_path)):
                    config_path = path.expanduser(default_path)
                    break
        if config_path:
            with open(config_path, 'r') as fp:
                config = yaml.load(fp.read())
                self._validate_config(config)
                return config
        raise PhilipException('No configuration file present')

    def _validate_config(self, config):
        if 'profiles' not in config:
            raise PhilipException('You must specify at least one "profile" in your configuration')
        for profile in config['profiles']:
            _profile = config['profiles'][profile]
            if 'provider' not in _profile:
                raise PhilipException('{} must specify a provider'.format(profile))
            if _profile['provider']['provider_type'] not in self.PROVIDERS:
                raise PhilipException('Unknown provider {}'.format(_profile['provider']['provider_type']))

    def get(self):
        for profile in reversed(self.profile_names):
            if profile in self.config['profiles']:
                profile = self.config['profiles'][profile]
                provider_type = profile['provider']['provider_type']
                if provider_type == 'marathon':
                    return MarathonServer(
                        profile,
                        profile['provider']['url'],
                        profile['provider']['username'],
                        profile['provider']['password']
                    )
                if provider_type == 'ecs':
                    return ECSConfig(
                        profile['provider']['cluster'],
                        profile['provider']['aws_config']
                    )
