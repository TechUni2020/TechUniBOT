from datetime import datetime
import base64
import json
import hmac
import hashlib
import os
import codecs

class JoinApplication:
    _DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"

    _appl_template_file = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "template", "join_application.md"))
    _appl_template = None
    def __init__(self, data: dict):
        # ID
        self.id: str = data["ID"]
        # 申請日時 ex) data内は、2024-01-01 01:11:11 +0900
        self.applied_at: datetime = (
            datetime.strptime(data["applied_at"], self._DATE_FORMAT)
        )
        # メールアドレス
        self.mail_address: str = data["mail_address"]

        # 申請者情報
        ap = data["applier"]
        # 氏名
        self.name: str = ap["name"]
        # 学校
        self.school: str = ap["school"]
        # 学部
        self.department: str = ap["department"]
        # 学年
        self.grade: str = ap["grade"]
        # 知ったきっかけ
        self.opportunity: str = ap["opportunity"]

        # 入会情報
        det = data["details"]
        # 入会理由
        self.reason: str = det["reason"]
        # やりたいこと
        self.goal: str = det["goal"]
        # 作りたいプロダクト
        self.product: str = det["product"]

    @staticmethod
    def from_webhook(data: dict, key: str):
        d: dict = data.copy()
        sign: str = d.pop("sign")

        secretkey_b: bytes = key.encode("utf-8")
        payload_b: bytes = base64.b64encode(
            json.dumps(d, separators=(',', ':'), ensure_ascii=False).encode("utf-8")
        )

        calc_sign = hmac.new(secretkey_b, payload_b, hashlib.sha256).hexdigest()
        if calc_sign != sign:
            raise ValueError("Invalid sign")
        return JoinApplication(d)

    def to_dict(self):
        return {
            "ID": self.id,
            "applied_at": self.applied_at.strftime(self._DATE_FORMAT),
            "mail_address": self.mail_address,
            "applier": {
                "name": self.name,
                "school": self.school,
                "department": self.department,
                "grade": self.grade,
                "opportunity": self.opportunity
            },
            "details": {
                "reason": self.reason,
                "goal": self.goal,
                "product": self.product
            }
        }

    @classmethod
    def from_template(cls) -> str:
        if cls._appl_template is None:
            with codecs.open(cls._appl_template_file, "r", "utf-8") as f:
                cls._appl_template = f.read()
        return cls._appl_template

    def create_initial_message(self):
        mes = self.from_template()
        for attr in vars(self):
            val = getattr(self, attr)
            mes = mes.replace(f"%%{attr}%%", str(val))
        return mes

    def __str__(self):
        # 全項目列挙
        return f"JoinApplication({self.id}, {self.applied_at}, {self.mail_address}, {self.name}, {self.school}, {self.department}, {self.grade}, {self.reason}, {self.opportunity}, {self.possible_dates})"
