import json


def print_json(result):
    print(json.dumps(result, sort_keys=True, indent=4))
