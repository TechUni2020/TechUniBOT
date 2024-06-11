import time
import imaplib
import email.utils
from email.message import EmailMessage
from email.header import Header
from techuni.email import EmailTemplate, EmailClientManager

class EmailController:
    def __init__(self, client_manager: EmailClientManager):
        self._client_manager = client_manager

    def send(self, template: EmailTemplate, to: str | list[str], args: dict):
        if isinstance(to, str):
            to: list[str] = [to]

        with self._client_manager.get(template.from_address) as from_client:
            msg = EmailMessage()
            msg["Message-ID"] = email.utils.make_msgid(domain=from_client.get_domain())
            msg["From"] = EmailController._encode_header(from_client.get_header())
            msg["To"] = ", ".join(to)
            msg["Subject"] = EmailController._encode_header(template.subject)
            msg["Date"] = email.utils.formatdate()
            msg["Organization"] = EmailController._encode_header(from_client.organization)

            for subtype in template.subtypes:
                content = template.get_template(subtype)
                for k, v in args.items():
                    content = content.replace(f"%%{k}%%", str(v))
                msg.add_alternative(content, subtype)

            from_client.smtp_server.send_message(msg)
            from_client.imap_server.append(
                from_client.get_box_name("Sent"),
                "\\Seen",
                imaplib.Time2Internaldate(time.time()),
                msg.as_string().encode("utf-8")
            )

        return msg

    @staticmethod
    def _format_content(template, obj):
        for attr in vars(obj):
            val = getattr(obj, attr)
            template = template.replace(f"%%{attr}%%", str(val))
        return template

    @staticmethod
    def _encode_header(content):
        return Header(content, "utf-8").encode(maxlinelen=0)
