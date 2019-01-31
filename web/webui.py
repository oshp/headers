# coding: utf-8
import os

from . import (
    api_header, api_headers
)
from flask import (
    Flask, g, send_from_directory,
    render_template, request, url_for,
    redirect, flash
)
from flask_caching import Cache
from flask_compress import Compress

from lib.utils.util import load_env_config
from lib.database.rdms_db import MySQL

from raven.contrib.flask import Sentry
from lib.utils.queries import (
    SELECT_SITE_HEADERS, GET_HTTP_HEADER_PERCENT
)

load_env_config()
db = MySQL()
compress = Compress()

app = Flask(__name__, static_folder="static")
app.secret_key = 'some_secret'
app.config['COMPRESS_MIMETYPES'] = os.getenv('MIME_TYPES').split(',')
app.register_blueprint(api_header.bp)
app.register_blueprint(api_headers.bp)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
if os.getenv("SENTRY_ENABLED"):
    sentry = Sentry(
        app,
        dsn='%s' % os.getenv(
            'SENTRY_DSN',
            'https://0b8820db003145838f2ce9b023df9687:295a00639ad44cfd9074a2f594702f6c@sentry.io/144923'))
    sentry = Sentry(app, dsn='%s' % os.getenv('SENTRY_DSN', ''))
compress.init_app(app)
cache.init_app(app)


@cache.cached(timeout=600)
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static/',
                               'service-worker.js')


@app.route('/')
def index():
    return redirect(url_for('summary'))


@cache.cached(timeout=86400)
@app.route('/summary')
def summary():
    return render_template('summary.html')


@cache.cached(timeout=86400)
@app.route('/about')
def about():
    return render_template('about.html')


@cache.cached(timeout=86400)
@app.route('/siteinfo', methods=['GET'])
@app.route('/siteinfo/<site>', methods=['GET'])
def siteinfo(site=''):
    '''Secure headers used by a specific <site>'''
    result = {}
    if site != '':
        configured_headers = db.query(SELECT_SITE_HEADERS.format(site_name=site))
        for header_name, header_value in configured_headers:
            percent_by_header = db.query(GET_HTTP_HEADER_PERCENT.format(header_name=header_name,
                                                                        header_value=header_value))
            result[header_name] = {header_value: percent_by_header[0]}
        if len(configured_headers) == 0:
            flash("This website was not found in our database.", 'notfound')
    if None in result:
        flash("This website has not HTTP secure headers set.", 'notset')
    return render_template('siteinfo.html',
                           site=site.lower(),
                           data=result)


@cache.cached(timeout=86400)
@app.route('/search_site', methods=['POST'])
def search_site():
    site = request.form['site']
    return redirect(url_for('siteinfo',
                            site=site))


# error pages
@cache.cached(timeout=86400)
@app.errorhandler(404)
@app.errorhandler(403)
def page_not_found(e):
    '''Redirect HTTP 404 code to 404.html template'''
    return render_template('404.html'), 404


@cache.cached(timeout=86400)
@app.errorhandler(500)
def internal_server_error(e):
    '''Redirect HTTP 500 code to 500.html template and set objects to
    caught user feedback sent to <sentry.io>'''
    return render_template('500.html',
                           event_id=g.sentry_event_id,
                           public_dsn=sentry.client.get_public_dsn('https')), 500


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src https://oshp.bsecteam.com https://js-agent.newrelic.com 'self'; " \
        "script-src https://oshp.bsecteam.com https://bam.nr-data.net https://js-agent.newrelic.com " \
        "https://ssl.google-analytics.com https://www.google-analytics.com https://ajax.cloudflare.com https://sentry.io https://cdn.ravenjs.com 'self'; " \
        "style-src https://oshp.bsecteam.com https://sentry.io 'self' 'unsafe-inline'; " \
        "img-src https://oshp.bsecteam.com https://sentry.io 'self'; " \
        "font-src https://oshp.bsecteam.com 'self'; " \
        "connect-src https://bam.nr-data.net https://js-agent.newrelic.com https://sentry.io 'self'; " \
        "manifest-src https://oshp.bsecteam.com 'self'; " \
        "object-src 'none'; " \
        "report-uri https://sentry.io/api/144923/csp-report/?sentry_key=0b8820db003145838f2ce9b023df9687"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response
