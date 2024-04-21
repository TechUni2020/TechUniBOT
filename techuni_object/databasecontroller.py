import os
import yaml
from supabase import create_client, Client
from .joinapply import JoinApply

class DatabaseController:
    def __init__(self, config_folder_path: str):
        fp = os.path.join(config_folder_path, 'supabase.yml')
        if not os.path.isfile(fp):
            raise FileNotFoundError("データベース認証情報ファイルが存在していません。")
        with open(fp) as f:
            db_auth = yaml.safe_load(f)
        self.db_client: Client = create_client(db_auth["URL"], db_auth["KEY"])

    def join_apply(self, applier: JoinApply):
        self.db_client.rpc("recieve_JoinApply", applier.to_dict()).execute()