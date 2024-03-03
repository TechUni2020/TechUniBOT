import os
import yaml
from joinapplier import JoinApplier

class DiscordController:
    def __init__(self, config_folder_path: str):
        fp = os.path.join(config_folder_path, 'discord.yml')
        if not os.path.isfile(fp):
            raise FileNotFoundError("DiscordBOT情報ファイルが存在していません。")
        with open(fp) as f:
            discord_bot_info = yaml.safe_load(f)
        self.endpoint = discord_bot_info["ENDPOINT"]

    def join_apply(self, applier: JoinApplier):
        pass