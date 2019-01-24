# Function framework for Python

This framework provides a mechanism to write Function-as-a-Service
style code in Python for handling CloudEvents delivered via HTTP.

This framework is primarily intended to work with
[Knative](https://github.com/knative/docs), but also works to provide
a generic server for handling CloudEvents over HTTP (e.g. from
Kubernetes or on a local machine).

Usage:

```python
import logging

from pyfun_events import Handle, Get

counter = 0


# @Handle assumes json body. For string or other body conversion, try:
# @Handle(str)
@Handle
def DoEvent(data: object, context: dict):
    logging.info(data)
    counter = counter + 1


@Handle(path="/secret")
def DoOther(data: object, context: dict):
    if data.get("handshake") == "backwards":
        counter = 0
        return "It's gone, man"


@Get
def Info():
    return "Got {0}".format(counter)


@Get("/dance")
def Party():
    return "<BLINK>Like it's 1999</BLINK>"
```


## Running manually

Copy `packaging/config.py` and `packaging/requirements.txt` into your
application directory alongside your other code. You can then start the Flask webserver running your function with:

```shell
FLASK_APP=config
flask run
```

## Running on Knative

There is a supplied build template in `packaging/build-template.yaml`, which you can apply to your cluster with:

```shell
kubectl apply -f packaging/build-template.yaml
```

or

```shell
kubectl apply -f https://github.com/evankanderson/pyfun/tree/master/packaging/build-template.yaml
```

Then update your Knative Service like so:

```diff
apiVersion: serving.knative.dev/v1alpha1
kind: Service
metadata:
  name: message-dumper
spec:
  runLatest:
    configuration:
+     build:
+       source:
+          git:
+            url: YOUR_REPO_URL
+            revision: HEAD
+       template:
+         name: pyfn
+         arguments:
+         - name: IMAGE
+           value: YOUR_DOCKER_IMAGE
+       serviceAccountName: builder
  revisionTemplate:
    spec:
      container:
        image: YOUR_DOCKER_IMAGE
```
