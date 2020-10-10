# docker-postfix-mailrelay
Based on boky/postfix, with simple support for sender_canonical and sender_bcc maps

## Usage
In addition to the boky/postfix image options, postmaps.sh will automatically create postmap files in /etc/postmaps on launch. This allows for injection of postmap hash files using kubernetes config like below:

```yaml
apiVersion: v1
data:
  sender_bcc_maps: |-
    # sender_address bcc_address
    robotman@doom.patrol cliff.steele@doom.manor
  sender_canonical_maps: |-
    # sender_address destination_rewrite
    # no change for trusted senders
    /^(cyborg@doom.patrol)$/ ${1}
    # no change for addresses containing noreply@
    /^(.*noreply@.*)$/ ${1}
    # expand empty addresses and missing domains
    /^$/ noreply@doom.patrol
    /^([^@]+)$/ ${1}+noreply@doom.patrol
    # rewrite addresses without noreply to include it
    /^(.+)@(.+)$/ ${1}+noreply@${2}
kind: ConfigMap
```
Then mount the vol and can use env vars to configure various maps. Note container will need to be restarted after a config map change to pick up changes.

## Mailfixer
The mailfixer container is a basic SMTP proxy built on aiosmtpd in python3 which inspects messages and fixes messages missing a body part/content-type. This can be used as a basis to do any type of message modification required above and beyond what is straightforward in postfix. To use it, just deploy it alongside the above postfix relay, expose port `8025`, and configure it's `REMOTE_HOSTNAME` and `REMOTE_PORT` parameters to point to postfix.

```python
from email.mime.text import MIMEText
from aiosmtpd.handlers import Proxy
from aiosmtpd.controller import Controller

proxy = Proxy(os.environ.get("REMOTE_HOSTNAME", "mail-relay"), os.environ.get("REMOTE_PORT", 587))


class FixerHandler:
    async def handle_DATA(self, server, session, envelope):
        statusmsg = "Message from {} to {}".format(envelope.mail_from, envelope.rcpt_tos)
        msg = email.message_from_string(envelope.content.decode("utf-8"))
        if msg.get_content_maintype() != "text":
            content_types = [part.get_content_type() for part in msg.get_payload()]
            if len([ct for ct in content_types if any(body_cts in ct for body_cts in ["plain", "html"])]) == 0:
                msg.set_payload([MIMEText("--", "plain")] + msg.get_payload())
                envelope.content = msg.as_string()
                envelope.original_content = msg.as_string().encode("utf-8")
                statusmsg += ": prepended TextBody '--'"
        print(statusmsg)
        return await proxy.handle_DATA(server, session, envelope)
```
