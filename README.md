# Function framework for Python

This framework provides a mechanism to write Function-as-a-Service style code in
Python for handling HTTP events, including CloudEvents delivered via HTTP.

This framework is primarily intended to work with
[Knative](https://knative.dev/), but also works to provide a generic server for
handling CloudEvents over HTTP (e.g. from Kubernetes or on a local machine).

The framework uses reflection to find a suitable function to wrap; it should not
be necessary to import any of the following modules in your own code unless you
want (e.g. for type definitions):

- `frameork` (this module; on PyPi as `http-containerize`)
- `flask`
- `cloudevents`

Instead, simply ensure that you have a single non-`_` prefixed function which
uses some combination of the following:

- HTTP request arguments (named `req`, `request`, `body`, `headers` or of the
  `flask.Request` type)
- CloudEvent arguments (named `event`, `payload`, `data`, `attributes` or of the
  `cloudevents.sdk.event.v1.Event` type)

Usage:

```python
import logging
from typing import Any


counter = 0


def DoEvent(data: Any, attributes: dict, req: Any):
    global counter
    counter = counter + 1

    logging.info(f"Got data: {data}")
    logging.info(f"From {req.origin}, my {counter}th request!")

    attributes["type"] = "com.example.reply"
    attributes["datacontenttype"] = "text/plain"

    return attributes, "It's a demo"

```

## Building into a container:

You can use the packeto buildpacks if you add `http-containerize>=0.4.0` to your `requirements.txt`:

```shell
pack build pytestapp --buildpack  ekanderson/pyfun:0.1.1 --builder paketobuildpacks/builder:base
```
You can then invoke it via:

```shell
docker run --rm -p 8080:8080 -e 8080 pytestapp
```