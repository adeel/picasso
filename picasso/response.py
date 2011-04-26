"Functions that turn various objects into Pack responses."

import collections
from pack.util.response import with_body, with_content_type

def render(response, request):
  "Render the object into a Pack response suitable for the given Pack request."

  if not response:
    return

  if not isinstance(response, dict):
    if callable(response):
      return render(
        response(request, **request.get("route_params", {})), request)
    response = with_body(response)

  response["body"] = _render_body(response.get("body"), request)
  if not response.get("headers", {}).get("content_type"):
    response = with_content_type(response, "text/html")

  return response

def _render_body(obj, request):
  if isinstance(obj, str) or isinstance(obj, unicode):
    return obj
  if isinstance(obj, file):
    return obj
  if isinstance(obj, collections.Iterable):
    return obj