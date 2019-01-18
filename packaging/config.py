from glob import glob
import importlib
import logging
import os.path
# This is needed to start gunicorn
from pyfun_events.run import app

if __name__ != '__main__':
    # Ensure logs go to the configured gunicorn location.
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    root_logger = logging.getLogger()
    root_logger.handlers = gunicorn_logger.handlers
    root_logger.setLevel(gunicorn_logger.level)

for f in glob('*.py'):
    if not os.path.isfile(f):
        continue
    logging.info(f'Importing {f[:-3]}')
    try:
        importlib.import_module(f[:-3])
    except ImportError as error:
        logging.exception(error)
        logging.error(f'Error importing {f}: {e}')
    except Exception as e:
        logging.error(f'Error importing {f}: {e}')
        continue
logging.info('Starting')
