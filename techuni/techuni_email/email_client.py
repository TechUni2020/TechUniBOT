import ssl
import email.utils
from smtplib import SMTP, SMTP_SSL
from imaplib import IMAP4, IMAP4_SSL

class EmailClient:
    def __init__(self, data: dict):
        self.address = str(data["address"])
        self.name = str(data["name"])
        self.organization = str(data["organization"])

        _smtp_data = data["smtp"]
        self.smtp_server = self._init_smtp(_smtp_data["ssl"], _smtp_data["host"], _smtp_data["port"], _smtp_data["user"], _smtp_data["password"])

        _imap_data = data["imap"]
        self.imap_server = self._init_imap(_imap_data["ssl"], _imap_data["host"], _imap_data["port"], _imap_data["user"], _imap_data["password"], _imap_data.get("ROOT", ""))

    def _init_smtp(self, ssl_type: str, host: str, port: int, user: str, password: str):
        _smtp_ssl = str(ssl_type).upper()
        if _smtp_ssl == "STARTTLS":
            server = SMTP(host, port)
            if not server.has_extn("STARTTLS"):
                raise RuntimeError(f"SMTP Server does not support STARTTLS. Address: {self.address} Name: {self.name}")
            context = ssl.create_default_context()
            server.starttls(context=context)

        elif _smtp_ssl == "SSL/TLS":
            context = ssl.create_default_context()
            server = SMTP_SSL(host, port, context=context)

        elif _smtp_ssl == "NONE":
            server = SMTP(host, port)

        else:
            raise ValueError(f"Invalid SSL Argument: {_smtp_ssl}. Address: {self.address} Name: {self.name}")

        server.login(user, password)
        return server

    def _init_imap(self, ssl_type: str, host: str, port: int, user: str, password: str, root_box: str):
        _imap_ssl = str(ssl_type).upper()
        if _imap_ssl == "STARTTLS":
            context = ssl.create_default_context()
            server = IMAP4(host, port)
            server.starttls(ssl_context=context)

        elif _imap_ssl == "SSL/TLS":
            context = ssl.create_default_context()
            server = IMAP4_SSL(host, port, ssl_context=context)

        elif _imap_ssl == "NONE":
            server = IMAP4(host, port)

        else:
            raise ValueError(f"Invalid SSL Argument: {_imap_ssl}. Address: {self.address} Name: {self.name}")

        server.login(user, password)
        self._IMAP_ROOT = root_box
        return server

    def get_box_name(self, box: str) -> str:
        return self._IMAP_ROOT + "." + box

    def get_domain(self) -> str:
        return self.address.split("@")[1]

    def get_header(self) -> str:
        return email.utils.formataddr((self.name, self.address))

    def __eq__(self, other):
        if not isinstance(other, EmailClient):
            return False
        return self.address == other.address

    def __hash__(self):
        return hash(self.address)
