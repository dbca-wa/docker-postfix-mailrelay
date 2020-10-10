FROM python:3
LABEL org.opencontainers.image.source https://github.com/dbca-wa/docker-postfix-mailrelay

WORKDIR /usr/src/app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8025

CMD [ "python", "./mailfixer.py" ]
