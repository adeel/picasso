"A middleware that turns a None response into a 404 Not Found response."

from pack.util.response import with_status, with_body

def wrap_not_found(app):
  """
  If none of the given routes match, the response will be None.  This
  will turn a None response into a 404 Not Found response, and is intended to
  the outermost middleware.
  """
  return lambda req: app(req) or with_status(with_body("Not Found"), 404)