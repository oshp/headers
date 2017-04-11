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
    'gevent==1.1.2',
    'mysql-connector==2.1.4',
    'argparse==1.4.0',
    'Flask==0.12',
    'raven==6.0.0',
    'blinker==1.4',
    'flask-compress==1.4.0',
    'Flask-Cache==0.13.1',
    'redis==2.10.5',
    'newrelic==2.82.0.62'
  ]
)
