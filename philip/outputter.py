import json

__author__ = 'leonmax'

def print_json(result):
    print(json.dumps(result, sort_keys=True, indent=4))
