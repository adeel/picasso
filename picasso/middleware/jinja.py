"A middleware that uses the Jinja templating system to render responses."

import os
from jinja2 import Environment, FileSystemLoader

def wrap_jinja(app, options={}):
  """
  If the app response is a tuple, will use Jinja2 to render the response.  The
  first element of the tuple is parsed as the template name, and the second
  should be a dictionary of data to be passed to the template.

    def view_product(req, id):
      # product = ...
      return "products/view", {"product": product}

  If sessions are enabled, a "session" key will be added to the data and sent
  to the template.

  Takes a template_dir option, which should be the path to your templates, and
  a config option, which can be a dict that will be passed to all your views.
  """

  options = dict({"template_dir": "./", "config": {}}, **options)

  template_dir = options["template_dir"]
  if not os.path.isdir(template_dir):
    raise Exception("Directory does not exist: %s" % template_dir)

  def wrapped(request):
    response = app(request)
    if isinstance(response.get("body"), tuple):
      if len(response["body"]) != 2:
        raise Exception(
          "picasso.middleware.jinja expected response to be a 2-element tuple,"
          " but got:\n  %s" % str(response["body"]))

      response["body"] = _render_with_jinja(options["template_dir"],
        *response["body"], session=request.get("session"),
                           flash=request.get("flash"),
                           config=options.get("config"))
      return response
    else:
      return response
  return wrapped

def _render_with_jinja(template_dir, template, data, session={}, flash={},
                       config={}):
  """
  Looks for the template in template_dir, and passes data to it.  Also adds a
  session key to the data, if sessions are enabled, and a flash key if the
  flash middleware is being used.
  """
  env = Environment(loader=FileSystemLoader(template_dir))
  data = dict(data, **config)

  # Add session key to data, if sessions are enabled.
  if session is not None:
    data["session"] = session
  if flash is not None:
    data["flash"] = flash

  return env.get_template(template + '.html').render(data).encode('utf-8')