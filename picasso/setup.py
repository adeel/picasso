# Some functions to create Pump apps from routes.

from pump.middleware.params import *
from pump.middleware.nested_params import *
from pump.middleware.cookies import *
from pump.middleware.session import *
from pump_jinja import *
from pump_flash import *
from picasso.middleware.not_found import *

# Generates a Pump app from the given routes that can be used for creating
# a web API.  Adds the following middleware:
#
#   - params
#   - nested_params
#
# (Does not add cookies and sessions.)
def setup_api(routes):
  app = routes
  for middleware in [wrap_not_found, wrap_nested_params, wrap_params]:
    app = middleware(app)
  return app

# Generates a Pump app from the given routes that are suitable for a
# typical website or web application.  Adds the following middleware:
#
#   - params
#   - nested_params
#   - sessions
#
# Options can contain "views" and "session" keys which will be passed to the
# jinja and session middlewares, respectively.
def setup_app(routes, options={}):
  app = routes
  app = wrap_not_found(app)
  app = wrap_jinja(app, options.get("views", {}))
  app = wrap_flash(app)
  app = wrap_session(app, options.get("session", {}))
  app = setup_api(app)
  return app