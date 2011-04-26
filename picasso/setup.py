"Functions that create Pack apps from routes."

from pack.middleware.params import *
from pack.middleware.nested_params import *
from pack.middleware.cookies import *
from pack.middleware.session import *
from picasso.middleware.jinja import *
from picasso.middleware.flash import *

def setup_api(routes):
  """
  Generates a Pack app from the given routes that can be used for creating
  a web API.  Adds the following middleware:

    -- params
    -- nested_params

  Does not add cookies and sessions.
  """
  app = routes
  for middleware in [wrap_nested_params, wrap_params]:
    app = middleware(app)
  return app

def setup_app(routes, options={}):
  """
  Generates a Pack app from the given routes that can be used for creating
  a typical website or web application.  Adds the following middleware:

    -- params
    -- nested_params
    -- sessions

  Options can contain "views" and "session" keys which will be passed to the
  jinja and session middlewares, respectively.
  """

  app = routes
  app = wrap_jinja(app, options.get("views", {}))
  app = wrap_flash(app)
  app = wrap_session(app, options.get("session", {}))
  app = setup_api(app)
  return app