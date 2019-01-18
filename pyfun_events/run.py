#!/usr/bin/python3
#
# A simple function to dump delivered events to stdout and report them
# via web page.

import logging
from glob import glob
import importlib
from inspect import signature, isfunction
import os.path

from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from flask import Flask, request
from typing import Callable, TypeVar, Mapping
import ujson

import pyfun_events.run


app = Flask(__name__)


def Handle(unpack: Callable[[str], object]=ujson.loads, path: str='/', **kwargs):
    """Decorate a function to handle events.

    Assumes func is a method which takes two arguments: data and context.
    data: provided the body of the event, processed via the unpack function.
    context: a dict containing cloudevents context attributes.
    """
    # It would be nice to support both decorating a function as
    # @Handle and @Handle(params). This is more difficult because
    # unpack is also a function, and the no-parens version of the
    # annotation will pass the function as the first
    # argument. Fortunately, a event-handling function takes at least
    # two arguments, so we can inspect the function to determine if we
    # are in the no-arg case.
    no_arg = False
    if isfunction(unpack) and len(signature(unpack).parameters) >= 1:
        no_arg = unpack
        unpack = ujson.loads
    def wrap(func: Callable[[object, dict], None]) -> None:
        def handle():
            m = marshaller.NewDefaultHTTPMarshaller()
            event = m.FromRequest(
                v02.Event(),
                request.headers,
                request.data,
                unpack)
            return func(event.Data(), event)

        pyfun_events.run.app.add_url_rule(path, func.__name__, handle, methods=['POST'], **kwargs)
    if no_arg:
        return wrap(no_arg)
    return wrap


def Get(path: str='/', **kwargs):
    """Decorate a function to respond to Get requests.
    """
    no_arg = False
    if callable(path):
        # Is actually a plain decorator
        no_arg = path
        path = '/'
    def wrap(func: Callable[[], None]) -> None:
        pyfun_events.run.app.add_url_rule(path, func.__name__, func, **kwargs)
    if no_arg:
        return wrap(no_arg)
    return wrap
