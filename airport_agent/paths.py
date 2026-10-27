"""Where everything lives. The read path (tools, agent, chat) only ever touches SERVING and CONFIG."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
SERVING = ROOT / "data" / "serving"
LOGS = ROOT / "logs"


def settings() -> dict:
    with open(CONFIG / "settings.yaml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)
