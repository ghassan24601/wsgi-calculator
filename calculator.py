"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback


def add(*args):
    """
    Add function
    :param args: list
    :return: string
    """
    try:
        total = sum(list(map(int, args)))
    except ValueError as ve:
        return "Please enter numeric values for the calculation. Error: {}".format(ve)
    return str(total)


def divide(*args):
    """
    Division function
    :param args: list
    :return: string
    """
    try:
        total = int(args[0]) / int(args[1])
    except ValueError:
        return "Please enter numeric values for the calculation."
    except ZeroDivisionError:
        return "Nice try. No dividing by zero. You know the rules."
    return str(total)


def multiply(*args):
    """
    Multiplication function
    :param args: list
    :return: string
    """
    try:
        total = int(args[0]) * int(args[1])
    except ValueError:
        return "Please enter numeric values for the calculation."
    return str(total)


def subtract(*args):
    """
    Subtraction function
    :param args: list
    :return: string
    """
    try:
        total = int(args[0]) - sum(list(map(int, args[1:])))
    except ValueError:
        return "Please enter numeric values for the calculation."
    return str(total)


def home_page():
    """
    Home page
    :return: string
    """
    body = "<h1>WSGI Calculator</h1>\n"
    body += "<h2>http://localhost:8080/match_func/no1/no2/...</h2>\n"
    body += "<h3>match_func: add, multiply, subtract, divide</h3>\n"
    body += "<h3>no1, no2: any integer number</h3>\n"
    return body


def resolve_path(path):
    """
    A function to resolve path routes
    :param path: string
    :return: function and its args
    """
    routes = {
      '': home_page,
      'add': add,
      'multiply': multiply,
      'subtract': subtract,
      'divide': divide
    }
    path = path.strip('/').split('/')
    func_name = path.pop(0)
    func = routes.get(func_name)
    args = path

    return func, args


def application(environ, start_response):
    """
    WSGI application
    :param environ:
    :param start_response:
    :return:
    """
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
