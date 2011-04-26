import pack

from setup import setup_api, setup_app
from routing import GET, POST, PUT, DELETE, HEAD, ANY

from pack.util.response import redirect, file_response

def setup_routes(*routes):
  """
  Create a Pack app from a list of compiled routes (see
  routing._compile_route).
  """
  return lambda req: routing.route(req, *routes)
