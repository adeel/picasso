# Generating Pump responses.

import collections
from pump.util.response import with_body, with_content_type

# Render the object into a Pump response suitable for the given Pump request.
def render(response, request):
  if not response:
    return

  if not isinstance(response, dict):
    # If the response is a function, call it and render the result.
    if callable(response):
      return render(
        response(request, **request.get("route_params", {})), request)
    response = with_body(response)

  response["body"] = _render_body(response.get("body"), request)
  # Default content_type is text/html.
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