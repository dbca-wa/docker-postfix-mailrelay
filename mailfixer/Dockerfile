LABEL org.opencontainers.image.source https://github.com/dbca-wa/docker-postfix-mailrelay
FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8025

CMD [ "python", "./mailfixer.py" ]
