import os
import sys
from techuni_object import JoinApplier, DatabaseController, DiscordController

# パス登録 - アプリケーションディレクトリ
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
# パス登録 - BOTディレクトリ
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'techuni_object')))

class TechUniBOT:
    def __init__(self, config_path: str):
        self.db_controller = DatabaseController(config_path)
        self.discord_controller = DiscordController(config_path)

    def join_apply(self, applier: dict | JoinApplier):
        if isinstance(applier, dict):
            applier = JoinApplier(applier)
        self.db_controller.join_apply(applier)
        self.discord_controller.join_apply(applier)


