# core/paths.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTAINERS_DIR = BASE_DIR / "containers"
LOGS_DIR = BASE_DIR / "logs"
