# core/process_manager.py
import subprocess
import threading
import time

class ContainerProcess:
    def __init__(self, config):
        self.config = config
        self.process = None
        self.output = []
        self.restart = config.get("restart", {}).get("on_crash", False)

    def start(self):
        cmd = self.config.get("start")
        if not cmd:
            raise RuntimeError(
                f"Container {self.config.get('name')} has no 'start' command"
            )

        self.process = subprocess.Popen(
            cmd,
            cwd=self.config["path"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        threading.Thread(target=self._read_output, daemon=True).start()
        threading.Thread(target=self._watchdog, daemon=True).start()

    def _read_output(self):
        """Читает stdout контейнера (live терминал)"""
        for line in self.process.stdout:
            self.output.append(line)
            print(f"[{self.config['name']}] {line}", end="")

    def _watchdog(self):
        """Следит за процессом и перезапускает при падении"""
        self.process.wait()
        if self.restart:
            delay = self.config.get("restart", {}).get("delay", 5)
            print(f"[{self.config['name']}] crashed, restarting in {delay}s...")
            time.sleep(delay)
            self.start()

    def stop(self):
        if self.process and self.is_running():
            self.process.terminate()

    def is_running(self):
        return self.process and self.process.poll() is None
