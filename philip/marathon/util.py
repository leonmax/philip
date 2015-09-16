# -*- coding: utf-8 -*-

import json


def print_response(response):
    if hasattr(response, 'text'):
        print(json.dumps(json.loads(response.text), indent=4))
    if isinstance(response, dict):
        print(json.dumps(response, indent=4))

