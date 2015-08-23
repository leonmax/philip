import copy


def merge(value1, value2):
    # completely replace d1 with d2
    if value2 is None:
        return copy.deepcopy(value1)
    if isinstance(value1, list):
        # if d1 is a list and d2 is not, merge d2 to every element in d1
        if not isinstance(value2, list):
            return [merge(v1, value2) for v1 in value1]
        # if both are lists, use the second
        else:
            # return value1 + value2
            return copy.deepcopy(value2)
    elif not isinstance(value1, dict) or not isinstance(value2, dict):
        # d1 is neither list nor list or d2 is not dict
        return copy.deepcopy(value2)
    else:
        return _merge_dicts(value1, value2)


def _merge_dicts(dict1, dict2):
    # merge dict1 and dict2
    result = copy.deepcopy(dict1)
    for key in dict2:
        if key in result:
            result[key] = merge(result[key], dict2[key])
        elif dict2[key] is not None:
            result[key] = dict2[key]
    return result
