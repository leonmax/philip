# phili
Philippides is the messager who delivered the news of victory from Marathon to Athens.
Phili is a small tool for deploying apps to [marathon](https://mesosphere.github.io/marathon/) and, of course, deliver the news of success from Marathon to the user.

currently only supports tags for docker apps, groups with tags are not supported. (if you don't need to update tag then it doesn't matter)

## Install
``` bash
pip install phili
```

## Configuration
By default it reads from:
`~/.config/phili/config.yml` or `~/.config/phili/config.json`
but you can specific config file by `phili -c config.json app.json` please reference to commandline help

``` yaml
stage:
    url: STAGE_MARATHON_URL
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
prod:
    url: PROD_MARATHON_URL
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
whatever:
    url: WHATEVER_MARATHON_URL
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
```

## Marathon artifact/group extension
first, like the configuration, you are allow to use either json or yaml
second, you can add profiles that can override the default content of the artifact/group configuration. the extended format is under the format like below

``` yaml
# you regular artifact/group config
# ...
setting1:
  setting1_2: 'being overwritten'
# end of the config
profiles:
  some_profile:
    setting1:
      setting1_2: 'overwrites'
    setting2: 'additions'
    # the config to override the regular ones
    # end of the overriding conf
  # other profiles ...
```

a more detailed sample:
``` yaml
id: python
instances: 1
cpus: 0.1
mem: 64.0
args: ["python", "-m", "http.server", "8000"]
container:
  type: DOCKER
  docker:
    image: python:3.4.3
    network: BRIDGE
profiles:
  stage:
    container:
      docker:
        portMappings:
          -
            containerPort: 8000
            servicePort: 10000
  prod:
    container:
      docker:
        portMappings:
          -
            containerPort: 8000
            servicePort: 10000
```

when specify your profile as stage (`phili -p stage app.yml`), you got a final config like below:

``` yaml
id: ./python-8001-10001
instances: 1
cpus: 0.1
mem: 64.0
args: ["python", "-m", "http.server", "8001"]
container:
  type: DOCKER
  docker:
    image: python:3.4.3
    network: BRIDGE
    portMappings:
      -
        containerPort: 8001
        servicePort: 10001
```

## Commandline Help
``` bash
phili -p prod apps.yaml
```
this will use the profile `prod` with it's url, username, password and overwrite the marathon artifact/group with the corresponding `profiles` section, please see `Marathon artifact/group extension`

Please read detail in `phili -h`: 
```
usage: phili.py [-h] [-p PROFILE] [-c CONFFILE] [-t TAG] [--dry-run] filename

positional arguments:
  filename              config filename

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        profile to run
  -c CONFFILE, --conffile CONFFILE
                        config file of the deployment script
  -t TAG, --tag TAG     docker tag
  --dry-run             dry run this deploy without really execute
```
