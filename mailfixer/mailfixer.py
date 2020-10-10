#!/usr/bin/env python
import os, time, email
from datetime import datetime
from email.mime.text import MIMEText
from aiosmtpd.handlers import Proxy
from aiosmtpd.controller import Controller

proxy = Proxy(os.environ.get("REMOTE_HOSTNAME", "mail-relay"), os.environ.get("REMOTE_PORT", 587))


class FixerHandler:
    async def handle_DATA(self, server, session, envelope):
        print("Message from {} to {} received at {}".format(envelope.mail_from, envelope.rcpt_tos, datetime.now().isoformat()))
        msg = email.message_from_string(envelope.content.decode("utf-8"))
        if msg.get_content_maintype() != "text":
            content_types = [part.get_content_type() for part in msg.get_payload()]
            if len([ct for ct in content_types if any(body_cts in ct for body_cts in ["plain", "html"])]) == 0:
                msg.set_payload([MIMEText("--", "plain")] + msg.get_payload())
                envelope.content = msg.as_string()
                envelope.original_content = msg.as_string().encode("utf-8")
                print("Inserted TextBody '--'")
        return await proxy.handle_DATA(server, session, envelope)


if __name__ == "__main__":
    handler = FixerHandler()
    controller = Controller(handler, hostname="0.0.0.0")
    # Run the event loop in a separate thread.
    controller.start()
    # Wait for an interrupt
    print("SMTP server running.")
    while time.sleep(900) is None:
        print("Still running: {}".format(datetime.now().isoformat()))
    controller.stop()
