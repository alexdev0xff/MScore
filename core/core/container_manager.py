# core/container_manager.py
import yaml
from core.paths import CONTAINERS_DIR

def load_containers():
    containers = []

    print(f"[ContainerManager] Scanning: {CONTAINERS_DIR}")

    if not CONTAINERS_DIR.exists():
        print("[ContainerManager] containers dir not found")
        return containers

    for folder in CONTAINERS_DIR.iterdir():
        if not folder.is_dir():
            continue

        config_file = folder / "container.yaml"
        if not config_file.exists():
            continue

        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        config["path"] = folder
        containers.append(config)

    return containers
