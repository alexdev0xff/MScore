# core/registry.py

from core.container_manager import load_containers
from core.process_manager import ContainerProcess

class ContainerRegistry:
    def __init__(self):
        self.containers = {}   # name -> config
        self.processes = {}    # name -> ContainerProcess

    def load(self):
        containers = load_containers()
        print(f"[Registry] Found {len(containers)} containers")

        for c in containers:
            name = c.get("name")
            print(f"[Registry] Loaded container: {name}")
            self.containers[name] = c

    def start(self, name):
        if name not in self.containers:
            raise ValueError(f"Container '{name}' not found")

        if name in self.processes and self.processes[name].is_running():
            print(f"[Registry] {name} already running")
            return

        proc = ContainerProcess(self.containers[name])
        proc.start()
        self.processes[name] = proc
        print(f"[Registry] {name} started")

    def stop(self, name):
        proc = self.processes.get(name)
        if not proc:
            print(f"[Registry] {name} not running")
            return

        proc.stop()
        print(f"[Registry] {name} stopped")

    def restart(self, name):
        self.stop(name)
        self.start(name)

    def send(self, name, command):
        proc = self.processes.get(name)
        if not proc or not proc.is_running():
            print(f"[Registry] {name} not running")
            return

        proc.send_command(command)

    def status(self):
        result = {}
        for name in self.containers:
            proc = self.processes.get(name)
            result[name] = "RUNNING" if proc and proc.is_running() else "STOPPED"
        return result

def load(self):
    containers = load_containers()
    print(f"[Registry] Found {len(containers)} containers")

    for c in containers:
        name = c.get("name")
        print(f"[Registry] Loaded container: {name}")
        self.containers[name] = c

    print("[Registry] Final containers:", self.containers.keys())


# singleton
registry = ContainerRegistry()
