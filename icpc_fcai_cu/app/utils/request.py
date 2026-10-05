import json

from icpc_fcai_cu.app.utils.responses import error_response


def parse_json(request):
    """Returns (body, error_response). Exactly one of them is None."""
    try:
        body = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, error_response(message="Invalid JSON body", status=400)

    if not isinstance(body, dict):
        return None, error_response(message="JSON body must be an object", status=400)

    return body, None