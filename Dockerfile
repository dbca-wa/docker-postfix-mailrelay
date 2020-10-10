FROM boky/postfix
LABEL org.opencontainers.image.source https://github.com/dbca-wa/docker-postfix-mailrelay

ADD postmaps.sh /docker-init.db/
