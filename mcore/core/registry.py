from core.monitor import get_process_stats
from core.ports import is_port_free
from core.container_manager import load_containers
from core.process_manager import ContainerProcess
import shutil


class ContainerRegistry:
    def __init__(self):
        self.containers = {}
        self.processes = {}

    def load(self):
        containers = load_containers()
        print(f"[Registry] Found {len(containers)} containers")

        for c in containers:
            name = c.get("name")
            print(f"[Registry] Loaded container: {name}")
            self.containers[name] = c

        print("[Registry] Final containers:", self.containers.keys())

    def start(self, name):
        if name not in self.containers:
            raise ValueError(f"Container '{name}' not found")

        self._check_ports(name)

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

    def kill(self, name):
        proc = self.processes.get(name)
        if not proc or not proc.is_running():
            print(f"[Registry] {name} not running")
            return

        proc.kill()
        print(f"[Registry] {name} killed")

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

    def stats(self):
        result = {}
        for name, proc in self.processes.items():
            s = get_process_stats(proc)
            if s:
                result[name] = s
        return result

    def attach(self, name):
        proc = self.processes.get(name)
        if not proc or not proc.is_running():
            print(f"[Registry] {name} not running")
            return

        print(f"[Attach] Connected to {name}")

        try:
            for line in proc.output[-100:]:
                print(line, end="")

            last_len = len(proc.output)

            while proc.is_running():
                if len(proc.output) > last_len:
                    for line in proc.output[last_len:]:
                        print(line, end="")
                    last_len = len(proc.output)

        except KeyboardInterrupt:
            print("\n[Attach] Detached")

    def remove(self, name):
        if name in self.processes and self.processes[name].is_running():
            self.stop(name)

        cfg = self.containers.get(name)
        if not cfg:
            raise ValueError(f"Container '{name}' not found")

        path = cfg["path"]

        self.processes.pop(name, None)
        self.containers.pop(name, None)

        shutil.rmtree(path)
        print(f"[Registry] {name} removed")

    def _check_ports(self, name):
     cfg = self.containers[name]
     ports = cfg.get("ports", [])

     if isinstance(ports, dict):
        ports = ports.values()

     ports = [int(p) for p in ports]

     for port in ports:
        for other, ocfg in self.containers.items():
            if other == name:
                continue

            oports = ocfg.get("ports", [])
            if isinstance(oports, dict):
                oports = oports.values()
            oports = [int(p) for p in oports]

            if port in oports:
                raise RuntimeError(f"Port {port} already reserved by {other}")

        if not is_port_free(port):
            raise RuntimeError(f"Port {port} already in use")


registry = ContainerRegistry()
