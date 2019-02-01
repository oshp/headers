FROM python:3.6.5-alpine

LABEL maintainer="alexandre menezes <alexandre.fmenezes@owasp.org>"

WORKDIR /app

COPY . .

RUN apk update && \
  apk add --no-cache gcc make build-base curl && \
  pip install -r requirements.txt && \
  rm -rf /var/cache/apt/*

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=4 \
  CMD curl http://localhost:5000/ || exit 1

ENV NEW_RELIC_LICENSE_KEY ''

ENTRYPOINT ["/app/docker/secureheaders/docker-entrypoint.sh"]
