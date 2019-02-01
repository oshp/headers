from lib.charts.datacharts import Datacharts

from flask import (
    Blueprint, jsonify
)


charts = Datacharts()
bp = Blueprint('api_headers',
               __name__,
               url_prefix='/api/v1/headers')


@bp.route('/total', methods=['GET'])
def headers_total():
    num_sites = charts.get_total_sites()
    return jsonify(num_sites)
