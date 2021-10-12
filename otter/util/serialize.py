import json

from collections.abc import Iterable


class OtterEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif getattr(obj, "values", None):
            return obj.values()
        return json.JSONEncoder.default(self, obj)


def to_json(items):
    return json.dumps(items, indent=4, cls=OtterEncoder)


def from_json(string):
    return json.loads(string)


def serialize(args, items):
    if items is None:
        return None
    if isinstance(items, str):
        return items
    if not isinstance(items, Iterable) or not items:
        raise Exception('data cannot be serialized')

    # items = sorted(items)
    # if args.format == 'json':
    return to_json(items)
    # else:
    #     return '\n'.join(str(i) for i in items)


def serialize_file(file, items):
    with open(file, 'w') as f:
        json.dump(items, f, indent=2)


def deserialize_file(file):
    with open(file, 'r') as f:
        string = f.read()

        if len(string) == 0:
            return dict()

        if file.lower().endswith(".json"):  # args.format == 'json' or
            return from_json(string)

    return None
