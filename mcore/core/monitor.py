# core/monitor.py
import psutil
import time

def get_process_stats(proc):
    if not proc or not proc.is_running():
        return None

    try:
        p = psutil.Process(proc.process.pid)

        cpu = p.cpu_percent(interval=0.1)
        mem = p.memory_info().rss // 1024 // 1024
        uptime = int(time.time() - p.create_time())

        return {
            "cpu": cpu,
            "memory": mem,
            "uptime": uptime
        }

    except psutil.NoSuchProcess:
        return None
