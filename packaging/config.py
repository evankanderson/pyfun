from glob import glob
import importlib
import os.path
# This is needed to start gunicorn
from pyfun_events.run import app

for f in glob('*.py'):
    if not os.path.isfile(f):
        continue
    print(f'Importing {f[:-3]}')
    try:
        importlib.import_module(f[:-3])
    except Exception as e:
        print(f'Error importing {f}: {e}')
        continue
print('Starting')
