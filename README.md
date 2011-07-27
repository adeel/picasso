# Picasso

Picasso is a simple web framework built on [Pump](http://adeel.github.com/pump).

## Examples

Here's a simple example demonstrating the use of routes, forms, sessions and redirects.

    from picasso import *

    def home(req):
      if not req["session"].get("user"):
        return redirect("/login")
      return "<h1>Welcome back, %s!</h1>" % req["session"]["user"]

    def login(req):
      return "<form method='post'><input type='submit' value='login' /></form>"

    def login_post(req):
      req["session"]["user"] = "James"
      return redirect("/")

    routes = setup_routes(
      GET("/", home),
      GET("/login", login),
      POST("/login", login_post),
      routing.not_found("<h1>Not Found</h1>"))

    app = setup_app(routes)
    pump.adapters.serve_with_paste(app)

Here's an [example blog](https://github.com/adeel/picasso-blog-example) written with Picasso.

## Installation

If you have pip, run

    $ pip install Picasso

or get the latest snapshot from Github with

    $ git clone git://github.com/adeel/picasso.git
    $ cd picasso
    $ python setup.py install

## License

Copyright (c) 2011 Adeel Ahmad Khan <adeel@adeel.ru>.

MIT license.