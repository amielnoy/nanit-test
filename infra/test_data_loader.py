import json
from pathlib import Path
from typing import List, Dict, Any

TEST_DATA_DIR = Path(__file__).resolve().parent.parent / "assets"


def load_login_users() -> List[Dict[str, Any]]:
    data_file = TEST_DATA_DIR / "login_users.json"
    with data_file.open("r", encoding="utf-8") as f:
        return json.load(f)
