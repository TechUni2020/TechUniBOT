import os
from yaml import safe_load
from enum import Enum, auto
from techuni.util import multi_dirname

_TEMPLATE_DIR: str = os.path.join(multi_dirname(__file__, 3), "template", "mail")
_TYPE_EXTENSION = {
    "html": "html",
    "plain": "txt"
}

class EmailTemplate(Enum):
    RECEIVE = auto(),
    INVITE = auto()

    def __init__(self, _id):
        self.id = _id
        self.is_init = False

        self.templates = {}
        self.subject: str
        self.subtypes: set

    def _load_info(self):
        # テンプレート情報をymlから読み込む
        with open(self._get_path_info(), "r") as f:
            _info = safe_load(f)
        self.subject = str(_info["subject"])  # メールの主題
        self.subtypes = set(_info.get("subtype", []))  # Content-Typeの一覧 keyがない場合、空
        if "plain" not in self.subtypes:
            self.subtypes.add("plain")

    def _load_template(self):
        for content_type in self.subtypes:
            with open(self._get_path(content_type), "r") as f:
                self.templates[content_type] = f.read()
        self.is_init = True

    def _get_path(self, content_type: str):
        return os.path.join(
            _TEMPLATE_DIR,
            self.name.lower(),
            f"{self.name.lower()}.{_TYPE_EXTENSION[content_type]}"
        )

    def _get_path_info(self):
        return os.path.join(
            _TEMPLATE_DIR,
            self.name.lower(),
            f"{self.name.lower()}.yml"
        )

    def get_template(self, content_type):
        if not self.is_init:
            raise ValueError("Template is not Loaded")
        return self.templates[content_type]

    @classmethod
    def load(cls):
        for template in cls:
            if template.is_init:
                continue
            template._load_info()
            template._load_template()
            template.is_init = True
