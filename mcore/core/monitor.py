# core/monitor.py
import psutil

def get_process_stats(pid):
    p = psutil.Process(pid)
    return {
        "cpu": p.cpu_percent(),
        "memory": p.memory_info().rss // 1024 // 1024
    }
