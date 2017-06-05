import os

from flask import Flask, g
from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_caching import Cache
from flask_compress import Compress

from lib.utils.util import Util
from lib.database.db import DB
from lib.charts.datacharts import Datacharts

from raven.contrib.flask import Sentry
from lib.utils.queries import SELECT_SITE_HEADERS
from lib.utils.queries import GET_HTTP_HEADER_PERCENT
from lib.utils.config import MIME_TYPES

settings = Util().load_config()
charts = Datacharts(settings)
db = DB(settings)
compress = Compress()

app = Flask(__name__, static_folder="static")
app.secret_key = 'some_secret'
app.config['COMPRESS_MIMETYPES'] = MIME_TYPES
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
sentry = Sentry(
    app,
    dsn='%s' % os.getenv(
        'SENTRY_DSN',
        'https://0b8820db003145838f2ce9b023df9687:295a00639ad44cfd9074a2f594702f6c@sentry.io/144923'))
#sentry = Sentry(app, dsn='%s' % os.getenv('SENTRY_DSN', ''))
compress.init_app(app)
cache.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('summary'))

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
    '''Secure headers used by a specific <url>'''
    values = ()
    percent_list = []
    if site != '':
        values = db.query(SELECT_SITE_HEADERS % site)
        for row in values:
            percent_list.append(
                db.query(
                    GET_HTTP_HEADER_PERCENT % (
                        row[0], row[0], row[1].replace("\"",""))))
        if len(values) == 0 or len(percent_list) == 0:
                flash("This website was not found in our database.")
    return render_template('siteinfo.html',
                           site=site.lower(),
                           data=zip(values, percent_list))

@cache.cached(timeout=86400)
@app.route('/search_site', methods=['POST'])
def search_site():
    site = request.form['site']
    return redirect(url_for('siteinfo', site=site))

@app.route('/xss_chart', methods=['POST'])
def xss_chart():
    xss_datacharts = charts.get_xss_datachart()
    return jsonify(xss_datacharts)

@app.route('/pkp_chart', methods=['POST'])
def pkp_chart():
    pkp_datacharts = charts.get_pkp_datachart()
    return jsonify(pkp_datacharts)

@app.route('/xfo_chart', methods=['POST'])
def xfo_chart():
    xfo_datacharts = charts.get_xfo_datachart()
    return jsonify(xfo_datacharts)

@app.route('/xcto_chart', methods=['POST'])
def xcto_chart():
    xcto_datacharts = charts.get_xcto_datachart()
    return jsonify(xcto_datacharts)

@app.route('/sts_chart', methods=['POST'])
def sts_chart():
    sts_datacharts = charts.get_sts_datachart()
    return jsonify(sts_datacharts)

@app.route('/csp_chart', methods=['POST'])
def csp_chart():
    csp_datacharts = charts.get_csp_datachart()
    return jsonify(csp_datacharts)

# error pages
@cache.cached(timeout=86400)
@app.errorhandler(403)
def page_not_found(e):
    '''Redirect HTTP 403 code to 403.html template'''
    return render_template('403.html'), 403

@cache.cached(timeout=86400)
@app.errorhandler(404)
def page_not_found(e):
    '''Redirect HTTP 404 code to 404.html template'''
    return render_template('404.html'), 404

@cache.cached(timeout=86400)
@app.errorhandler(500)
def page_not_found(e):
    '''Redirect HTTP 500 code to 500.html template and set objects to
    caught user feedback sent to <sentry.io>'''
    return render_template('500.html',
                           event_id=g.sentry_event_id,
                           public_dsn=sentry.client.get_public_dsn('https')
                           ), 500

@app.after_request
def apply_caching(response):
    response.headers["Content-Security-Policy"] = "base-uri 'self'; " \
        "media-src 'none'; " \
        "img-src 'self'; " \
        "script-src 'self' http://oshp.bsecteam.com https://www.google-analytics.com https://ssl.google-analytics.com https://js-agent.newrelic.com https://ajax.cloudflare.com https://cdnjs.cloudflare.com; " \
        "font-src 'self' https://cdnjs.cloudflare.com; " \
        "form-action 'self' http://oshp.bsecteam.com"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block; report=https://oshp.bsecteam.com/xssreport"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response
