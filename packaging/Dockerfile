FROM python:3.7-alpine

WORKDIR /app

# Copy the framework and application's requirements.txt and run pip to
# install all dependencies. Alpine doesn't include gcc by default, so
# install that before pip.
COPY framework/requirements.txt /app/framework/requirements.txt
COPY requirements.txt /app/requirements.txt
RUN /bin/ash -c 'apk add build-base && pip install -r /app/framework/requirements.txt && pip install -r /app/requirements.txt'

# Add the application source code.
ADD . /app

# Run a WSGI server to serve the application.
CMD gunicorn -b :$PORT --access-logfile - --error-logfile - framework.config:app
