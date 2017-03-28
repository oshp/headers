# SecureHeaders  
[![Build Status](https://travis-ci.org/amenezes/secureheaders.svg?branch=master)](https://travis-ci.org/amenezes/secureheaders)
[![Dependency Status](https://gemnasium.com/badges/github.com/amenezes/headers.svg)](https://gemnasium.com/github.com/amenezes/headers)
[![Code Quality](https://codeclimate.com/github/amenezes/headers/badges/gpa.svg)](https://codeclimate.com/github/amenezes/headers)
[![Code Health](https://landscape.io/github/amenezes/secureheaders/master/landscape.svg?style=flat)](https://landscape.io/github/amenezes/secureheaders/master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/24f73ab5fb144dafbd30d043570c7444/badge.svg)](https://www.quantifiedcode.com/app/project/24f73ab5fb144dafbd30d043570c7444)

OWASP SecureHeaders Project  

SecureHeaders project consist in two main modules:
1. an engine to scan a list of sites fastly and with minimal resources;
2. a web interface with a dashboard to view, search and customize besides
provide insight and feedback about the use of HTTP secure headers.

HTTP secure headers are resources known to some and despised by others.
However it's a fact that the versatility and security provided by feature can
help make web applications more secure.

### Architecture

![SecureHeaders Architecture](https://dl.dropboxusercontent.com/u/6427240/oshp/secureheaders.png)

### Web Interface

![SecureHeaders Main Page](https://dl.dropboxusercontent.com/u/6427240/oshp/oshp_main.png)
The SecureHeaers webui provide an easyly way to see and search all data
gathering with scanner module. For now it's possible to see a dashboard
with main HTTP secure headers documented OWASP web page and also provide
a way to search secure headers set in each page analyzed as your adoption
by other users.

#### Dependencies  
- docker engine
- docker-compose

#### Installation
```bash
docker-compose up -d
```

### Scanner

[![asciicast](https://asciinema.org/a/ehee1olc3qys1wbdz1zqmiu84.png)](https://asciinema.org/a/ehee1olc3qys1wbdz1zqmiu84)
The scanner module it's responsible to catch all secure headers data from csv list.

> notice: the module work, however it is under rebuild process to make it more effective,
robust and much better.

##### Dependencies  

Check [requirements-txt](https://github.com/amenezes/headers/blob/master/requirements.txt).

##### Installation
```bash
pip install -r requirements-txt
```  

### More

See the [wiki page](https://github.com/oshp/headers/wiki) to see more
about how to use, contribute and much more.
