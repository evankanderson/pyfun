# Python Cloud Events Function

Welcome to your new Python function project! A small working function can be
found in `main.py`, which responds to (transforms) CloudEvents.

When adding to this module, note that you must have exactly one public (non-"_"
prefixed) function which which matches the expected function signature (all
arguments have defaults or match the patterns described below). You may also
create an `__init__.py` which exports a single such function if you wish to
disambiguate between multiple public functions.

## Arguments

The framework will fill in any of the following function parameters by `name` or
_type_.

- _event_ or _cloudevents.sdk.event.v1.Event_: a CloudEvent object
- `payload` or `data`: the CloudEvents `data` attribute, decoded
- `attributes`: a dictionary of CloudEvents attributes
- `req`, `request` or _flask.Request_: an HTTP request object
- `headers`: a dictionary of the HTTP request headers

## Running locally:

```shell
pip install http-containerize
python -m framework
```

## Building into a container:

```shell
pack build pytestapp --buildpack  ekanderson/pyfun:0.1.1 --builder paketobuildpacks/builder:base
```
You can then invoke it via:

```shell
docker run --rm -p 8080:8080 -e 8080 pytestapp
```

It's also expected that you should be able (soon) to run this via [kn-plugin-func](https://github.com/knative-sandbox/kn-plugin-func):

```shell
kn func create -l python -t http
kn func run
```
