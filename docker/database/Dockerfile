FROM mysql:5.5.54

LABEL org.owasp.oshp.name="Owasp SecureHeaders Project Database" \
  org.owasp.oshp.description="SecureHeaders Project Database" \
  org.owasp.oshp.url="https://www.owasp.org/index.php/OWASP_Secure_Headers_Project" \
  org.owasp.oshp.version="v3.1.0" \
  org.owasp.oshp.maintainer="alexandre menezes <alexandre.fmenezes@owasp.org>"

ENV HEADERS_FILE https://dl.dropboxusercontent.com/u/6427240/headers.sql

RUN apt-get update && apt-get -y install curl \
  && curl -o headers.sql $HEADERS_FILE \
  && mv headers.sql /docker-entrypoint-initdb.d/

HEALTHCHECK --timeout=5s --start-period=30s --retries=3 \
  CMD curl localhost:3306

USER mysql
