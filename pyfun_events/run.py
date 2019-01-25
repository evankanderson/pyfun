#!/usr/bin/python3
#
# A simple function framework

from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from flask import Flask, request
from typing import Any, Callable, Optional, TypeVar, Union, overload, cast
import ujson

app = Flask(__name__)

T = TypeVar('T')

Handler = Callable[[Any, dict], None]

GetHandler = Callable[[], None]

@overload
def Handle(path: Handler) -> Handler:
    ...

@overload
def Handle(
      path: str="/",
      unpack: Callable[[str], T]=ujson.loads,
      **kwargs) -> Callable[[Callable[[T, dict], None]], Callable[[T, dict], None]]:
    ...

def Handle(
    path: Union[str, Handler]='/',
    unpack: Callable[[str], Any]=ujson.loads,
    **kwargs):
    """Decorate a function to handle events.

    Assumes func is a method which takes two arguments: data and context.
    data: provided the body of the event, processed via the unpack function.
    context: a dict containing cloudevents context attributes.
    """
    no_arg = None  # type: Optional[Handler]
    if not isinstance(path, str):
        no_arg = cast(Handler, path)
        path = '/'
    def wrap(func: Handler) -> Handler:
        def handle():
            m = marshaller.NewDefaultHTTPMarshaller()
            event = m.FromRequest(
                v02.Event(),
                request.headers,
                request.data,
                unpack)
            return func(event.Data(), event)
        app.add_url_rule(path, func.__name__, handle, methods=['POST'], **kwargs)
        return func
    if no_arg:
        return wrap(no_arg)
    return wrap

@overload
def Get(path: GetHandler) -> GetHandler:
    ...

@overload
def Get(path: str='/', **kwargs) -> Callable[[GetHandler], GetHandler]:
    ...

def Get(path: Union[str, GetHandler]='/', **kwargs):
    """Decorate a function to respond to Get requests.
    """
    no_arg = None  # type: Optional[GetHandler]
    if not isinstance(path, str):
        no_arg = cast(GetHandler, path)
        path = '/'
    def wrap(func: Callable[[], None]) -> None:
        app.add_url_rule(path, func.__name__, func, **kwargs)
    if no_arg:
        return wrap(no_arg)
    return wrap
