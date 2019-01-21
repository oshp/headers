# SecureHeaders 

[![Build Status](https://travis-ci.org/oshp/headers.svg?branch=master)](https://travis-ci.org/oshp/headers)
[![Maintainability](https://api.codeclimate.com/v1/badges/9abf0feda40825b531a9/maintainability)](https://codeclimate.com/github/oshp/headers/maintainability)
[![Code Health](https://landscape.io/github/amenezes/secureheaders/master/landscape.svg?style=flat)](https://landscape.io/github/amenezes/secureheaders/master)

OWASP SecureHeaders Project  

SecureHeaders project consist in two main modules:
1. an engine to scan a list of sites fastly and with minimal resources;
2. a web interface with a dashboard to view, search and customize besides
provide insight and feedback about the use of HTTP secure headers.

HTTP secure headers are resources known to some and despised by others.
However it's a fact that the versatility and security provided by feature can
help make web applications more secure.

### Architecture

![SecureHeaders Architecture](https://www.dropbox.com/s/wkxdksye9oqxwpd/secureheaders.png?raw=1)

### Web Interface

![SecureHeaders Main Page](https://dl.dropboxusercontent.com/u/6427240/oshp/oshp_main.png)
The SecureHeaers webui provide an easyly way to see and search all data
gathering with scanner module. For now it's possible to see a dashboard
with main HTTP secure headers documented OWASP web page and also provide
a way to search secure headers set in each page analyzed as your adoption
by other users.

#### Installation
##### dependencies
1. mysql
2. redis
##### docker
```bash
docker-compose up -d
```
##### bare metal
````bash
# install virtualevn
#
pip install virtualenv
# create virtualenv locally
#
virtualenv venv
# active virtualenv
#
source venv/bin/activate
# install application dependencies
#
pip install -r requirements.txt
# start application (web interface)
#
gunicorn -w 2 -b 0.0.0.0:5000 web.webui:app
````

### Scanner
##### dependencies

1. mysql
##### docker
````bash
docker-compose -f docker-compose.scanner.yml up -d
````

##### bare metal

###### overview:  

[![asciicast](https://asciinema.org/a/ehee1olc3qys1wbdz1zqmiu84.png)](https://asciinema.org/a/ehee1olc3qys1wbdz1zqmiu84)
The scanner module it's responsible to catch all secure headers data from a csv file.

###### setup, install and run scanner:

````bash
# install virtualevn
#
pip install virtualenv
# create virtualenv locally
#
virtualenv venv
# active virtualenv
#
source venv/bin/activate
# install application dependencies
#
pip install -r requirements.txt
# start application (web interface)
#
python cli.py
````

````bash
# sample scanner help output
# python cli.py --help
#
Usage: cli.py [OPTIONS]

  OWASP SecureHeaders Project [OSHP] will analyze and  provides an overview
  about http secure headers specify from a CSV list.

Options:
  --version              Show the version and exit.
  -f, --file TEXT        topsites file path.  [default:
                         conf/topsites_global.csv]
  -t, --threads INTEGER  number of threads.  [default: 1000]
  --help                 Show this message and exit.
````

##### Dependencies  

check [requirements.txt](https://github.com/amenezes/headers/blob/master/requirements.txt).

### More

See the [wiki page](https://github.com/oshp/headers/wiki) to see more
about how to use, contribute and much more.