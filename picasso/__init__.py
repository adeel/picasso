import pump

from setup import setup_api, setup_app
from routing import GET, POST, PUT, DELETE, HEAD, ANY

from pump.util.response import redirect, file_response

# Create a Pump app from a list of compiled routes (see
# routing.compile_route).
def setup_routes(*routes):
  return lambda req: routing.route(req, *routes)
