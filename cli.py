import click
import os

from lib.utils.util import load_env_config
from lib.scanner.headers import Headers

load_env_config()

@click.command()
@click.version_option(version='4.0.0', 
                      prog_name='Owasp SecureHeader Scanner')
@click.option('-f', 
              '--file',
              'filename',
              show_default=True,
              default=os.getenv('TOPSTIES_FILENAME'),
              help='topsites file path.')
@click.option('-t', 
              '--threads',
              'threads_number',
              type=int,
              show_default=True,
              default=os.getenv('THREAD_NUMBER'), 
              help='number of threads.')
def start(filename, threads_number):
    """
     OWASP SecureHeaders Project [OSHP] will analyze and 
     provides an overview about http secure headers specify from a CSV list.
    """
    Headers().run(filename, threads_number)


if __name__ == '__main__':
    start()