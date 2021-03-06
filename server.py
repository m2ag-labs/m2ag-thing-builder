#!/usr/bin/env python
"""
Starts a Tornado static file server in a given directory.
To start the server in the current directory:
    tserv .
Then go to http://localhost:8000 to browse the directory.
Use the --prefix option to add a prefix to the served URL,
for example to match GitHub Pages' URL scheme:
    tserv . --prefix=jiffyclub
Then go to http://localhost:8000/jiffyclub/ to browse.
Use the --port option to change the port on which the server listens.
"""

from __future__ import print_function

import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import tornado.ioloop
import tornado.httpserver
import tornado.web


class Handler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path = url_path + 'index.html'
        return url_path


def mkapp(prefix=''):
    if prefix:
        path = '/' + prefix + '/(.*)'
    else:
        path = '/(.*)'

    application = tornado.web.Application([
        (path, Handler, {'path': os.getcwd()}),
    ], debug=False)

    return application


def start_server(prefix='', port=None):
    app = mkapp(prefix)
    if os.path.isfile(f'{str(Path.home())}/.m2ag-labs/ssl/server.crt') \
            and os.path.isfile(f'{str(Path.home())}/.m2ag-labs/ssl/server.crt'):
        ssl_options = {
            'certfile': f'{str(Path.home())}/.m2ag-labs/ssl/server.crt',
            'keyfile': f'{str(Path.home())}/.m2ag-labs/ssl/server.key',
        }
        if port is None:
            port = 8443
    else:
        ssl_options = None
        if port is None:
            port = 8080
    http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


def parse_args(args=None):
    parser = ArgumentParser(
        description=(
            'Start a Tornado server to serve static files out of a '
            'given directory and with a given prefix.'))
    parser.add_argument(
        '-f', '--prefix', type=str, default='',
        help='A prefix to add to the location from which pages are served.')
    parser.add_argument(
        '-p', '--port', type=int, default=8443,
        help='Port on which to run server.')
    parser.add_argument(
        '-d', '--dir', type=str, default='client', help='Directory from which to serve files.')
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    os.chdir(args.dir)
    print('m2ag.labs client service beta 1.0')
    print('copyright 2021 https://m2aglabs.com')
    print('Starting server on port {}'.format(args.port))
    start_server(prefix=args.prefix, port=args.port)


if __name__ == '__main__':
    sys.exit(main())
