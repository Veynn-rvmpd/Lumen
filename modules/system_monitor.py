"""
Hardware Telemetry & Host System Health Monitor.
Collects real-time metrics for CPU, RAM, disk partitions, and network I/O
using psutil without blocking overhead or graphical artifacts.
"""

import os
import platform
import time
from typing import Dict, Any
import psutil

SYSTEM_BOOT_TIME = psutil.boot_time()


def collect_system_telemetry() -> Dict[str, Any]:
    """
    Samples active hardware metrics across processors, memory arrays, and storage volumes.
    """
    cpuUsagePercent = psutil.cpu_percent(interval=None)
    cpuCores = psutil.cpu_count(logical=True)
    memoryMetrics = psutil.virtual_memory()

    try:
        diskMetrics = psutil.disk_usage(os.path.abspath(os.sep))
        diskTotalGb = round(diskMetrics.total / (1024 ** 3), 1)
        diskUsedGb = round(diskMetrics.used / (1024 ** 3), 1)
        diskPercent = diskMetrics.percent
    except Exception:
        diskTotalGb = 0.0
        diskUsedGb = 0.0
        diskPercent = 0.0

    networkCounters = psutil.net_io_counters()
    uptimeSeconds = int(time.time() - SYSTEM_BOOT_TIME)
    uptimeHours = round(uptimeSeconds / 3600.0, 1)

    # Determine executive status state
    if cpuUsagePercent > 85.0 or memoryMetrics.percent > 90.0:
        systemHealth = "[ALERT]"
    elif cpuUsagePercent > 70.0 or memoryMetrics.percent > 75.0:
        systemHealth = "[WARN]"
    else:
        systemHealth = "[OK]"

    return {
        "status": systemHealth,
        "hostName": platform.node(),
        "platform": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
        "uptimeHours": uptimeHours,
        "cpuPercent": cpuUsagePercent,
        "cpuCores": cpuCores,
        "memoryPercent": memoryMetrics.percent,
        "memoryUsedGb": round(memoryMetrics.used / (1024 ** 3), 2),
        "memoryTotalGb": round(memoryMetrics.total / (1024 ** 3), 2),
        "diskPercent": diskPercent,
        "diskUsedGb": diskUsedGb,
        "diskTotalGb": diskTotalGb,
        "netBytesSentMb": round(networkCounters.bytes_sent / (1024 ** 2), 2),
        "netBytesRecvMb": round(networkCounters.bytes_recv / (1024 ** 2), 2),
        "activeProcessesCount": len(psutil.pids())
    }


def get_executive_summary() -> str:
    """
    Formats a concise, single-paragraph text summary suitable for terminals or notifications.
    """
    telemetry = collect_system_telemetry()
    return (
        f"{telemetry['status']} LUMEN Host: {telemetry['hostName']} | "
        f"CPU: {telemetry['cpuPercent']}% | "
        f"RAM: {telemetry['memoryPercent']}% ({telemetry['memoryUsedGb']}/{telemetry['memoryTotalGb']} GB) | "
        f"Disk: {telemetry['diskPercent']}% | "
        f"Uptime: {telemetry['uptimeHours']}h | "
        f"Active PIDs: {telemetry['activeProcessesCount']}"
    )
