import pack

from setup import setup_api, setup_app
from routing import GET, POST, PUT, DELETE, HEAD, ANY

from pack.util.response import redirect, file_response

# Create a Pack app from a list of compiled routes (see
# routing._compile_route).
def setup_routes(*routes):
  return lambda req: routing.route(req, *routes)
