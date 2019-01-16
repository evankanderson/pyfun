#!/usr/bin/python3
#
# A simple function to dump delivered events to stdout and report them
# via web page.

import logging
from glob import glob
import importlib
import os.path

from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from flask import Flask, request
from typing import Callable, TypeVar, Mapping
import ujson

import pyfun_events.run


app = Flask(__name__)


def Handle(func: Callable[[object, dict], None]) -> None:
    """Invoke func whenever an event occurs.

    Assumes func is a method which takes two arguments: data and context.
    data: type T, which should be able to be constructed from a string.
    context: a dict containing cloudevents context information.
    """
    def handle():
        m = marshaller.NewDefaultHTTPMarshaller()
        event = m.FromRequest(
            v02.Event(),
            request.headers,
            request.stream,  # Maybe request.data?
            ujson.load)
        return func(event.Data(), event)

    pyfun_events.run.app.add_url_rule('/', 'handle', handle, methods=['POST'])


def Get(func: Callable[[], None]) -> None:
    """Invoke the specified func on Get requests.
    """
    pyfun_events.run.app.add_url_rule('/', 'get', func)


if __name__ == '__main__':
    for f in glob('*.py'):
        if not os.path.isfile(f):
            continue
        print('Importing {0}'.format(f[:-3]))
        try:
            importlib.import_module(f[:-3])
        except Exception as e:
            print('Error importing {0}: {1}'.format(f, e))
            continue
    print('Starting')
    run.app.run(debug=True)
