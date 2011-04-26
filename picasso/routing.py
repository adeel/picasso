import collections
from routes.base import Route
from routes.mapper import Mapper as RouteMapper
import response

def route(request, *routes):
  """
  Try to apply each route to the given request, returning the first nonempty
  response.  The routes need to have been compiled to functions with
  _compile_route.
  """
  for route in routes:
    response = route(request)
    if response:
      return response
  return {"status": 404}

methods = ["get", "post", "put", "delete", "head", "any"]
GET, POST, PUT, DELETE, HEAD, ANY = [lambda p, b, m=m:
  _compile_route(m, p, b) for m in methods]

not_found = lambda b: GET('/{url:.*}', b)

def _compile_route(method, path, body):
  """
  Compile the route into a Pack app.  The app will return the body given if and
  only if a matching route is found.  Otherwise it will return None.
  """
  def app(request):
    return response.render(body, request)
  return _if_method(method,
    _if_route(_prepare_route(path),
      app))

def _if_method(method, app):
  "Evaluate the app if the method matches the request."
  def wrapped(request):
    if not method or method == request.get("method") or method == "any":
      return app(request)
    elif method == "get" and request.get("method") == "head":
      response = app(request)
      if response:
        response["body"] = None
      return response
  return wrapped

def _if_route(route, app):
  "Evaluate the app if the route matches the request."
  def wrapped(request):
    params = _route_matches(route, request)
    if params is not None:
      return app(_set_route_params(request, params))
  return wrapped

def _set_route_params(request, params):
  "Set the \"route_params\" and \"params\" keys in the request."
  return _recursive_merge(request, {"route_params": params, "params": params})

def _route_matches(route, request):
  "Return the params of the route matching the request, if there is one."
  m = RouteMapper()
  m.extend([route])
  return m.match(request["uri"])

def _prepare_route(route):
  """
  Returns an instance of routes.base.Route (from the Routes package).  If
  route is a tuple, the first item should be a route and the second should be
  a dict with conditions on the params in the route.

    prepare_route("products/view/:id")
    prepare_route(("products/view/:id", {"id": r"\d+"}))
  """
  if isinstance(route, str) or isinstance(route, unicode):
    return Route(None, route)
  if isinstance(route, collections.Iterable):
    return Route(None, route[0], requirements=route[1])

def _recursive_merge(x, y):
  "Merge two dictionaries recursively."

  z = x.copy()
  for key, val in y.iteritems():
    if isinstance(val, dict):
      if not z.has_key(key):
        z[key] = {}
      z[key] = _recursive_merge(z[key], val)
    else:
      z[key] = val
  return z