import logging
from typing import Any


counter = 0


def DoPost(req: Any):
    # Fill in this function
    global counter
    counter = counter + 1

    logging.info(f"From {req.origin}, my {counter}th request!")

    return f"Hello, {req.form.get("user", default="stranger")}!"
