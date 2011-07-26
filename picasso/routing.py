import collections

from pack.util.response import with_body, with_status
from routes.base import Route
from routes.mapper import Mapper as RouteMapper

from picasso import response

# Try to apply each route to the given request, returning the first nonempty
# response.  The routes need to have been compiled to functions with
# _compile_route.
def route(request, *routes):
  for route in routes:
    response = route(request.copy())
    if response:
      return response

# Functions for each method that generate routes from a path and response.
# Supported methods: GET, POST, PUT, DELETE, and HEAD.
# ANY will match any method.
methods = ["get", "post", "put", "delete", "head", "any"]
GET, POST, PUT, DELETE, HEAD, ANY = [lambda p, b, m=m:
  compile_route(m, p, b) for m in methods]

# Generates a route that matches any URL and returns the given body.
# You can add it as your last route to get a custom 404 page.
def not_found(body):
  return ANY('/{url:.*}', body)

# Compile the route into a Pack app that will return the body given if and
# only if a matching route is found.  Otherwise it will return None.
def compile_route(method, path, body):
  def app(request):
    return response.render(body, request)
  return if_method(method, if_route(prepare_route(path), app))

# Call the app if the method matches the request.
def if_method(method, app):
  def wrapped(request):
    if not method or method == request.get("method") or method == "any":
      return app(request)
    elif method == "get" and request.get("method") == "head":
      response = app(request)
      if response:
        response["body"] = None
      return response
  return wrapped

# Call the app if the route matches the request.
def if_route(route, app):
  def wrapped(request):
    params = route_matches(route, request)
    if params is not None:
      return app(set_route_params(request, params))
  return wrapped

# Set the "route_params" and "params" keys in the request.
def set_route_params(request, params):
  return recursive_merge(request, {"route_params": params, "params": params})

# Return the params of the route matching the request, if there is one.
def route_matches(route, request):
  m = RouteMapper()
  m.extend([route])
  return m.match(request["uri"])

# Returns an instance of routes.base.Route (from the Routes package).  If
# route is a tuple, the first item should be a route and the second should be
# a dict with conditions on the params in the route.
#
#     prepare_route("products/view/:id")
#     prepare_route(("products/view/:id", {"id": r"\d+"}))
def prepare_route(route):
  if isinstance(route, str) or isinstance(route, unicode):
    return Route(None, route)
  if isinstance(route, collections.Iterable):
    return Route(None, route[0], requirements=route[1])

# Merge two dictionaries recursively.
def recursive_merge(x, y):
  z = x.copy()
  for key, val in y.iteritems():
    if isinstance(val, dict):
      if not z.has_key(key):
        z[key] = {}
      z[key] = recursive_merge(z[key], val)
    else:
      z[key] = val
  return z