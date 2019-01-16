# pyfun
Knative function framework for Python

Usage:

```python
import logging

from pyfun_events import Handle,Get

counter = 0

@Handle
def DoEvent(data :str, context: dict):
    logging.info(data)
    counter = counter + 1

@Get
def Info():
    return 'Got {0}'.format(counter)
```
