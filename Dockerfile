LABEL org.opencontainers.image.source https://github.com/dbca-wa/docker-postfix-mailrelay
FROM boky/postfix
ADD postmaps.sh /docker-init.db/
