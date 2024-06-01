import time
import imaplib
import email.utils
from email.message import EmailMessage
from techuni.techuni_email import EmailTemplate, EmailClientManager
from techuni.techuni_object import JoinApplication, JoinApplicationStatus

class EmailController:
    def __init__(self, client_manager: EmailClientManager):
        self._client_manager = client_manager

    def send(self, template: EmailTemplate, to: str | list[str], args: dict):
        if isinstance(to, str):
            to: list[str] = [to]

        from_client = self._client_manager.get(template.from_address)
        msg = EmailMessage()
        msg["Message-ID"] = email.utils.make_msgid(domain=from_client.get_domain())
        msg["From"] = from_client.get_header()
        msg["To"] = ", ".join(to)
        msg["Subject"] = template.subject
        msg["Date"] = email.utils.formatdate()
        msg["Organization"] = from_client.organization

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

    def send_joinapplication(self, application: JoinApplication, status: JoinApplicationStatus, additional_args: dict | None = None):
        if not status.need_send_email():
            raise ValueError(f"Email is not needed. ({status.name})")
        template = status.get_email_template()

        args = {}
        for attr in vars(application):
            args[attr] = str(getattr(application, attr))

        if additional_args is not None:
            args |= additional_args

        msg = self.send(template, application.mail_address, args)
        return msg

    @staticmethod
    def _format_content(template, obj):
        for attr in vars(obj):
            val = getattr(obj, attr)
            template = template.replace(f"%%{attr}%%", str(val))
        return template
