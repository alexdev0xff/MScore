import subprocess
import threading
import time
import os


class ContainerProcess:
    def __init__(self, config):
        self.config = config
        self.name = config.get("name", "unknown")
        self.process = None
        self.output = []

        startup = config.get("startup", {})
        restart_cfg = startup.get("restart", {})

        self.restart = restart_cfg.get("on_crash", False)
        self.restart_delay = restart_cfg.get("delay", 5)

    def _build_env(self):
        env = os.environ.copy()

        java = self.config.get("java", {})
        server = self.config.get("server", {})

        env["JAVA_BIN"] = java.get("bin", "java")
        env["JAVA_XMS"] = java.get("xms", "1024M")
        env["JAVA_XMX"] = java.get("xmx", "1024M")
        env["JAVA_FLAGS"] = " ".join(java.get("flags", []))

        env["SERVER_JAR"] = server.get("jar", "server.jar")
        env["SERVER_ARGS"] = " ".join(server.get("args", []))

        return env

    def start(self):
        startup = self.config.get("startup", {})
        cmd = startup.get("command")

        if not cmd:
            raise RuntimeError(f"Container {self.name} has no startup.command")

        env = self._build_env()

        self.process = subprocess.Popen(
            cmd,
            cwd=self.config["path"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
            start_new_session=True
        )

        threading.Thread(target=self._read_output, daemon=True).start()
        threading.Thread(target=self._watchdog, daemon=True).start()

        print(f"[Process] {self.name} started")

    def _read_output(self):
        for line in self.process.stdout:
            self.output.append(line)

    def _watchdog(self):
        self.process.wait()
        if self.restart:
            print(f"[{self.name}] crashed, restarting in {self.restart_delay}s...")
            time.sleep(self.restart_delay)
            self.start()

    def send_command(self, command):
        if self.is_running():
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

    def stop(self):
        if self.is_running():
            self.send_command("stop")

    def kill(self):
        if self.is_running():
            self.process.kill()

    def is_running(self):
        return self.process is not None and self.process.poll() is None
