FROM alpine:latest

LABEL org.owasp.oshp.url="https://www.owasp.org/index.php/OWASP_Secure_Headers_Project" \
  org.owasp.oshp.name="Owasp SecureHeaders Project" \
  org.owasp.oshp.description="Front-end from SecureHeaders Project" \
  org.owasp.oshp.version="v3.x" \
  org.owasp.oshp.maintainer="alexandre menezes <alexandre.fmenezes@owasp.org>"

ENV APP_DIR /opt/headers
ENV NEW_RELIC_LICENSE_KEY ''

ARG BRANCH=master
ARG URL=https://github.com/oshp/headers.git

WORKDIR $APP_DIR

RUN apk add --no-cache py2-pip py-setuptools gcc make build-base python2-dev git curl \
  && git clone --depth 1 $URL -b $BRANCH . \
  && pip2 install --upgrade pip \
  && pip2 install -r requirements.txt

EXPOSE 5000

COPY docker/secureheaders/docker-entrypoint-apm.sh /docker-entrypoint.sh

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=4 \
  CMD curl http://localhost:5000/ || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
