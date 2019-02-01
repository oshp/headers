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

## Architecture

![SecureHeaders Architecture](https://www.dropbox.com/s/wkxdksye9oqxwpd/secureheaders.png?raw=1)

## Dependencies  

- MySQL
- Redis
- Python 3.6

## Configuration (Dashboard | Scanner)

Edit `.env` file or set environment variable:

````txt
# general settings
## scanner
THREAD_NUMBER=1000
TOPSTIES_FILENAME=conf/topsites_global.csv
SENTRY_ENABLED=False
SENTRY_DSN=''

# http settings
ORIGIN=http://a.com
TIMEOUT=3

# mysql settings
MYSQL_USERNAME=root
MYSQL_PASSWORD=password
MYSQL_HOST=localhost
MYSQL_DATABASE=headers

# redis settings
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_TTL=60

# http header filters
HEADERS=strict-transport-security,public-key-pins,x-xss-protection,x-frame-options,x-content-type-options,content-security-policy,x-permitted-cross-domain-policies,referrer-policy

# plugins settings
MIME_TYPES=text/html,text/html; charset=utf-8,text/css,text/xml,application/json,image/png,application/javascript,image/jpeg
````

## Usage

````bash
# python cli.py --help
#
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  scanner  Owasp SecureHeader scanner.
  web      Owasp SecureHeader web dashboard
````

### scanner

````bash
# python cli.py scanner --help
#
Usage: cli.py scanner [OPTIONS]

  Owasp SecureHeader scanner.

Options:
  --version              Show the version and exit.
  -f, --file PATH        topsites file path.  [default:
                         conf/topsites_global.csv]
  -t, --threads INTEGER  number of threads.  [default: 1000]
  --help                 Show this message and exit.
````

### dashboard

````bash
# python cli.py web --help
#
Usage: cli.py web [OPTIONS] COMMAND

  Owasp SecureHeader web dashboard

Options:
  --help  Show this message and exit.
````

> valid command to start is: `./cli.py web start`

## Scanner Advanced

### docker

````bash
docker-compose -f docker-compose.scanner.yml up -d
````

### bare metal

#### mysql setup overview:

[![asciicast](https://asciinema.org/a/ehee1olc3qys1wbdz1zqmiu84.png)](https://asciinema.org/a/ehee1olc3qys1wbdz1zqmiu84)
The scanner module it's responsible to catch all secure headers data from a csv file.

#### setup, install and run scanner:

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
python cli.py scanner -f conf/develop.csv
Thread pool 1 (0 - 1000)
[*] connection error for <pclady.com.cn>
[!] site <pclady.com.cn> will be excluded from the analysis

Connections summary
https: 3
http: 2
error: 2

Cleaning database
Tables: [header, site, header_value, header_name]

Populating database...
Table: site
Table: header_value
Table: header_name
Table: header
````

## Dashboard Advanced

![SecureHeaders Main Page](https://s3.amazonaws.com/reports.bsecteam.com/dashboard.png)
The SecureHeaers webui provide an easyly way to see and search all data
gathering with scanner module. For now it's possible to see a dashboard
with main HTTP secure headers documented OWASP web page and also provide
a way to search secure headers set in each page analyzed as your adoption
by other users.

### Installation

#### docker

```bash
docker-compose -f docker-compose.dashboard.yml up -d
```
#### bare metal

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
python cli.py web start
starting web dashboard...
[*] application started on: http://localhost:5000/
[*] press any key to stop...
````

### More

See the [wiki page](https://github.com/oshp/headers/wiki) to see more
about how to use, contribute and much more.
