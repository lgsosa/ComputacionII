import json
from datetime import datetime

def _default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"tipo no serializable: {type(obj)}")

def to_json(data):
    return json.dumps(data, default=_default_serializer).encode("utf-8")

def from_json(raw):
    return json.loads(raw.decode("utf-8"))
