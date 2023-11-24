import json


def to_dict(a):
    """Return relevant data from an annotatios object as a dict"""
    data = {}

    if a.arch:
        data["arch"] = a.arch
    if a.flavour:
        data["flavour"] = a.flavour
    if a.flavour_dep:
        data["flavour_dep"] = a.flavour_dep
    if a.include:
        data["include"] = a.include
    if a.config:
        config = dict(a.config)
        for _, val in config.items():
            # Weed out internal "oneline" keys
            if "oneline" in val:
                del val["oneline"]
        data["config"] = config

    return data


def load_json(d):
    """Return JSON file content"""
    with open(d, encoding="utf-8") as fh:
        return json.load(fh)
