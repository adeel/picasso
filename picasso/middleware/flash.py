"A middleware for adding flash message support via sessions."

def wrap_flash(app):
  """
  Adds a "flash" key to the request that contains the current flash dict, which
  is stored in the session (request["session"]["flash"]).  If it is modified by
  the app, the session is updated accordingly.

  Note that request["flash"] is actually a dict-like object whose values
  disappear after the first access.
  """

  def wrapped(request):
    request["flash"] = DisappearingDict(request["session"].get("flash", {}))
    response = app(request)
    request["session"]["flash"] = request["flash"]
    return response
  return wrapped

class DisappearingDict(dict):
  "Like a dict, but values disappear after the first access."

  def __getitem__(self, key):
    val = dict.__getitem__(self, key)
    self.__setitem__(key, None)
    return val

  def get(self, key, d=None):
    if self.has_key(key):
      val = dict.__getitem__(self, key)
      self.__setitem__(key, None)
      return val
    return d