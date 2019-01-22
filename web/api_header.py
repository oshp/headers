import functools

from lib.secureheaders.xss import XXssProtection
from lib.secureheaders.csp import ContentSecurityPolicy
from lib.secureheaders.pkp import PublicKeyPins
from lib.secureheaders.sts import StrictTransportSecurity
from lib.secureheaders.xfo import XFrameOptions
from lib.secureheaders.xcto import XContentTypeOptions
from lib.secureheaders.rpolicy import ReferrerPolicy
from lib.secureheaders.xpcdp import XPermittedCrossDomainPolicies

from flask import (
    Blueprint, request, jsonify
)


bp = Blueprint('api', __name__, url_prefix='/api/v1/header')

@bp.route('/x-xss-protection', methods=['GET'])
def x_xss_protection():
    return jsonify(XXssProtection().get_datachart())


@bp.route('/public-key-pins', methods=['GET'])
def public_key_pins():
    return jsonify(PublicKeyPins().get_datachart())

@bp.route('/referrer-policy', methods=['GET'])
def referer_policy():
    return jsonify(ReferrerPolicy().get_datachart())

@bp.route('/x-permitted-cross-domain-policies', methods=['GET'])
def x_permitted_cross_domain_policies():
    return jsonify(XPermittedCrossDomainPolicies().get_datachart())

@bp.route('/x-frame-options', methods=['GET'])
def x_frame_options():
    return jsonify(XFrameOptions().get_datachart())


@bp.route('/x-content-type-options', methods=['GET'])
def x_content_type_options():
    return jsonify(XContentTypeOptions().get_datachart())


@bp.route('/strict-transport-security', methods=['GET'])
def strict_transport_security():
    return jsonify(StrictTransportSecurity().get_datachart())


@bp.route('/content-security-policy', methods=['GET'])
def content_security_policy():
    return jsonify(ContentSecurityPolicy().get_datachart())