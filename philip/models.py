import copy
import json
import yaml
from philip.exceptions import PhilipException


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


def merge(d1, d2):
    # completely replace d1 with d2
    if d2 is None:
        return copy.deepcopy(d1)
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        # if d1 is a list and d2 is not, merge d2 to every element in d1
        if isinstance(d1, list) and not isinstance(d2, list):
            return [merge(v1, d2) for v1 in d1]
        else:
            return copy.deepcopy(d2)
    result = copy.deepcopy(d1)
    for key in d2:
        if key in result:
            result[key] = merge(result[key], d2[key])
        elif d2[key] is not None:
            result[key] = d2[key]
    return result


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
