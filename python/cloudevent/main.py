import logging
from typing import Any


counter = 0


def DoEvent(data: Any, attributes: dict):
    # Fill in this function
    global counter
    counter = counter + 1

    logging.info(f"Got event {counter} data: {data}")

    # TODO: fill in response attributes with something meaningful.
    attributes["source"] = "http://transform-function.local/"
    attributes["type"] = "com.example.reply"
    attributes["datacontenttype"] = "text/plain"

    return attributes, "It's a reply"
