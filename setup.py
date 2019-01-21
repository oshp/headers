import os

from setuptools import setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

about = {}
with open(os.path.join(ROOT, "lib", "__about__.py")) as f:
    exec (f.read(), about)

setup(
  name=about["__title__"],
  version=about["__version__"],
  author=about["__author__"],
  author_email=about["__email__"],
  url=about["__uri__"],
  description=about["__summary__"],
  license=about["__license__"],
  packages=[],
  install_requires=[
    'appdirs==1.4.3',
    'atomicwrites==1.2.1',
    'attrs==18.2.0',
    'blinker==1.4',
    'certifi==2018.11.29',
    'chardet==3.0.4',
    'Click==7.0',
    'contextlib2==0.5.5',
    'Flask==1.0.2',
    'Flask-Caching==1.4.0',
    'Flask-Compress==1.4.0',
    'gevent==1.4.0',
    'greenlet==0.4.15',
    'gunicorn==19.9.0',
    'idna==2.8',
    'itsdangerous==1.1.0',
    'Jinja2==2.10',
    'MarkupSafe==1.1.0',
    'more-itertools==5.0.0',
    'mysql-connector==2.1.6',
    'newrelic==4.10.0.112',
    'packaging==18.0',
    'pathlib==1.0.1',
    'pluggy==0.8.1',
    'py==1.7.0',
    'pyparsing==2.3.0',
    'pytest==4.1.1',
    'python-dotenv==0.10.1',
    'raven==6.10.0',
    'redis==3.0.1',
    'requests==2.21.0',
    'six==1.12.0',
    'urllib3==1.24.1',
    'Werkzeug==0.14.1'
  ]
)
