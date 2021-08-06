from collections import namedtuple
import importlib.util
import inspect
import pathlib
import sys
import typing
import types

import flask
from flask.wrappers import Request
import cloudevents.http
import cloudevents.sdk.event.base

def FindFunc(dir: str) -> typing.Callable:
    workspace = pathlib.Path(dir).resolve()

    candidates = []
    if (workspace / "__init__.py").is_file():
        print("Importing from init.py")
        candidates.append(workspace / "__init__.py")
    else:
        for file in workspace.glob("*.py"):
            if file.stem.endswith("_test"):
                continue
            print(f"Importing from {file}")
            candidates.append(file)

    functions = []
    sys.path.insert(0, str(workspace))
    for f in candidates:
        spec = importlib.util.spec_from_file_location(f.stem, f)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        functions.extend(_FuncFromModule(module))
    sys.path.pop(0)

    if len(functions) == 1:
        return functions[0]
    return None

def _FuncFromModule(module : types.ModuleType) -> list[typing.Callable]:
    found = []
    for (name, x) in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("_"):
            continue
        sig = inspect.signature(x)
        print(f">>{name}: {sig}")
        sig = _MatchSignature(x)
        if sig is not None:
#        if issubclass(next(iter(sig.parameters.values())).annotation, cloudevents.sdk.event.base.BaseEvent):
#            x = _ConvertEvent(x)
#        elif next(iter(sig.parameters)) in ("event", "payload"):
#            x = _ConvertEvent(x)
            print(f">>> Matched sig {sig}")
            found.append(x)
                
    return found


def _ConvertEvent(func: typing.Callable) -> typing.Callable:
    def wrapper(request: flask.Request):
        event = cloudevents.http.from_http(request.headers, request.get_data())
        # TODO: support payload, attributes format
        out_event = func(event)
        headers, body = cloudevents.http.to_binary(out_event)
        return flask.Response(body, 200, headers)
    print(f"$$ Converting {inspect.signature(func)} to {inspect.signature(wrapper)}")
    return wrapper

# Each function signature has a "score" based on the quality/likelihood that
# this is the intended function signature. Higher numbers are better; multiple
# signatures may have the same score.
_Signature = namedtuple("_Signature", ['typelist', 'score', 'converter'])
_SIGNATURES = [
    _Signature((cloudevents.sdk.event.base.BaseEvent,), 10, _ConvertEvent),
    _Signature((flask.Request,), 10, None),
    _Signature(("event",), 6, _ConvertEvent),
    _Signature(("payload", "attributes"), 6, _ConvertEvent),
    _Signature(("payload",), 6, _ConvertEvent),
    _Signature(("attributes",), 6, _ConvertEvent),
    _Signature(("req",), 6, None),
    _Signature(("request",), 6, None),
    _Signature(("body",), 6, None),
    _Signature(("body", "headers"), 6, None),
    _Signature(("headers",), 6, None),
]

def _MatchSignature(func: typing.Callable) -> _Signature:
    sig = inspect.signature(func)
    params = [(k, v) for k, v in sig.parameters.items()]
    for s in _SIGNATURES:
        if len(params) != len(s.typelist):
            continue
        for want, got in zip(s.typelist, params):
            if isinstance(want, str):
                if got[0] != want:
                    break
            else:
                if not issubclass(got[1].annotation, want):
                    break
        else:
            return s

    if len(params) == 1:
        return _Signature((params[1].annotation), 2, None)

    return _Signature((), 0, None)
