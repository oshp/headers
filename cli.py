#!/usr/bin/env python
import click
import os
import subprocess

from lib.utils.util import load_env_config
from lib.scanner.headers import Headers

load_env_config()

@click.group()
def scanner_cli():
    pass

@scanner_cli.command()
@click.version_option(version='4.0.0', 
                      prog_name='Owasp SecureHeader Scanner')
@click.option('-f',
              '--file',
              'filename',
              show_default=True,
              type=click.Path(exists=True, readable=True),
              default=os.getenv('TOPSITES_FILENAME'),
              help='topsites file path.')
@click.option('-t', 
              '--threads',
              'threads_number',
              type=int,
              show_default=True,
              default=os.getenv('THREAD_NUMBER'),
              help='number of threads.')
def scanner(filename, threads_number):
    """ Owasp SecureHeader scanner. """
    Headers().run(filename, threads_number)

@click.group()
def web_cli():
    pass

@web_cli.command()
@click.argument('command')
def web(command):
    """ Owasp SecureHeader web dashboard """
    if command == 'start':
        click.echo('starting web dashboard...')
        process = subprocess.Popen(["gunicorn", "-w 2", "-b 0.0.0.0:5000", "web.webui:app"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        click.echo("[*] application started on: http://localhost:5000/")
        click.pause("[*] press any key to stop...")
        process.kill()
    else:
        click.echo('[*] valid commands is: [start]')


cli = click.CommandCollection(sources=[scanner_cli, web_cli])


if __name__ == '__main__':
    cli()
