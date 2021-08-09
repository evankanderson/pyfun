from collections import namedtuple
import importlib.util
import inspect
import pathlib
import sys
import typing
import types

import flask
import cloudevents.http
import cloudevents.sdk.event.base as ce_sdk


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


def _FuncFromModule(module: types.ModuleType) -> typing.List[typing.Callable]:
    found = []
    for (name, x) in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("_"):
            continue
        sig = inspect.signature(x)
        print(f">>{name}: {sig}")
        for arg in sig.parameters.values():
            convert = ArgumentConversion(arg)
            if not convert.valid:
                break
        else:
            print(f">>> Matched sig {sig}")
            found.append(x)

    return found


class ArgumentConversion:
    def __init__(self, p: inspect.Parameter):
        self.name = p.name
        self._convert = None
        self.need_event = False
        self.unknownArg = None
        TYPE_TO_TRANSLATION = {
            ce_sdk.BaseEvent: (lambda x: x, True),
            flask.Request: (lambda x: x, False),
        }
        NAME_TO_TRANSLATION = {
            "event": (lambda x: x, True),
            "data": (lambda x: x.data, True),
            "payload": (lambda x: x.data, True),
            "attributes": (lambda x: {k:x[k] for k in x}, True),
            "req": (lambda x: x, False),
            "request": (lambda x: x, False),
            "body": (lambda x: x.get_data(), False),
            "headers": (lambda x: x.headers, False),
        }
        if p.annotation in TYPE_TO_TRANSLATION:
            self._convert, self.need_event = TYPE_TO_TRANSLATION[p.annotation]
        if p.name in NAME_TO_TRANSLATION:
            self._convert, self.need_event = NAME_TO_TRANSLATION[p.name]

        if self._convert is None and p.default == inspect.Parameter.empty:
            if p.kind not in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                self.unknownArg = p

    def convert(self, req: flask.Request, ce: ce_sdk.BaseEvent = None) -> typing.Any:
        if not self.valid:
            raise ValueError(f"Unable to convert {self.p} to a function argument.")
        if self.need_event:
            return self._convert(ce)
        return self._convert(req)

    @property
    def valid(self) -> bool:
        return self.unknownArg is None
