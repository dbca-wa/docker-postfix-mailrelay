#!/usr/bin/env python
import os, email, logging, asyncio
from email.mime.text import MIMEText
from aiosmtpd.handlers import Proxy
from aiosmtpd.controller import Controller

proxy = Proxy(os.environ.get("REMOTE_HOSTNAME", "mail-relay"), os.environ.get("REMOTE_PORT", 587))


class FixerHandler:
    async def handle_DATA(self, server, session, envelope):
        print("Message from {} to {}".format(envelope.mail_from, envelope.rcpt_tos))
        msg = email.message_from_string(envelope.content.decode("utf-8"))
        if msg.get_content_maintype() != "text":
            content_types = [part.get_content_type() for part in msg.get_payload()]
            if len([ct for ct in content_types if any(body_cts in ct for body_cts in ["plain", "html"])]) == 0:
                msg.set_payload([MIMEText("--", "plain")] + msg.get_payload())
                envelope.content = msg.as_string()
                envelope.original_content = msg.as_string().encode("utf-8")
                print("Inserted TextBody '--'")
        return await proxy.handle_DATA(server, session, envelope)


async def amain(loop):
    handler = FixerHandler()
    controller = Controller(handler, hostname="0.0.0.0", port=8025)
    controller.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop=loop))
    try:
        print("SMTP server running.")
        loop.run_forever()
    except KeyboardInterrupt:
        pass
