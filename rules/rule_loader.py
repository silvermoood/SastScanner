import json
from .rule import Rule


def load_rules(path):
    with open(path) as f:
        data = json.load(f)

    return [Rule(rule) for rule in data]
