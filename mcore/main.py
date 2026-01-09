# core/main.py
import time
from core.registry import registry


class McoreDaemon:
    def __init__(self):
        self.running = True

    def banner(self):
        print("================================")
        print("       Mcore daemon start        ")
        print("================================")

    def load_containers(self):
        registry.load()

        if not registry.containers:
            print("[Mcore] No containers found")
        else:
            print(f"[Mcore] Loaded {len(registry.containers)} container(s)")

    def autostart(self):
        for name, cfg in registry.containers.items():
            if cfg.get("startup", {}).get("auto_start"):
                registry.start(name)

    def cli(self):
        print("Commands:")
        print("  start <name>")
        print("  stop <name>")
        print("  restart <name>")
        print("  status")
        print("  exit")

        while self.running:
            try:
                cmd = input("mcore> ").strip()
            except EOFError:
                break

            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0]

            try:
                if action == "start" and len(parts) == 2:
                    registry.start(parts[1])

                elif action == "stop" and len(parts) == 2:
                    registry.stop(parts[1])

                elif action == "restart" and len(parts) == 2:
                    registry.restart(parts[1])

                elif action == "status":
                    statuses = registry.status()
                    stats = registry.stats()

                    for name, state in statuses.items():
                        line = f"{name}: {state}"

                        if state == "RUNNING" and name in stats:
                            s = stats[name]
                            line += (
                                f" | CPU {s['cpu']:.1f}%"
                                f" | RAM {s['memory']} MB"
                                f" | uptime {s['uptime']}s"
                            )

                        print(line)

                elif action in ("exit", "quit"):
                    self.shutdown()

                else:
                    print("Unknown command")

            except Exception as e:
                print(f"[ERROR] {e}")

    def shutdown(self):
        print("\n[Mcore] Shutting down...")
        self.running = False

        for name in list(registry.processes.keys()):
            registry.stop(name)

    def run(self):
        self.banner()
        self.load_containers()
        self.autostart()
        print("[Mcore] Daemon is running")
        self.cli()


def main():
    daemon = McoreDaemon()
    daemon.run()


if __name__ == "__main__":
    main()
