"""Health check and monitoring service for the library system."""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import sys

from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class HealthService:
    """
    Service for performing health checks and system monitoring.

    Provides diagnostic information about the system status,
    storage availability, and overall health.
    """

    def __init__(self) -> None:
        """Initialize the health service."""
        self.start_time = datetime.now()
        logger.info("HealthService initialized")

    def check_health(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check.

        Returns:
            Dictionary containing health status information.
        """
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "checks": {}
        }

        # Check storage availability
        storage_check = self._check_storage()
        health_status["checks"]["storage"] = storage_check

        # Check logs directory
        logs_check = self._check_logs()
        health_status["checks"]["logs"] = logs_check

        # Check Python version
        health_status["checks"]["python"] = {
            "status": "healthy",
            "version": sys.version,
            "version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro
            }
        }

        # Check disk space
        disk_check = self._check_disk_space()
        health_status["checks"]["disk"] = disk_check

        # Determine overall status
        failed_checks = [
            name for name, check in health_status["checks"].items()
            if check.get("status") != "healthy"
        ]

        if failed_checks:
            health_status["status"] = "unhealthy"
            health_status["failed_checks"] = failed_checks
            logger.warning(f"Health check failed: {failed_checks}")
        else:
            logger.debug("Health check passed")

        return health_status

    def _check_storage(self) -> Dict[str, Any]:
        """Check if storage directories are accessible."""
        data_dir = Path("data")

        try:
            data_dir.mkdir(exist_ok=True)

            # Try to write a test file
            test_file = data_dir / ".health_check"
            test_file.write_text("OK")
            test_file.unlink()

            return {
                "status": "healthy",
                "writable": True,
                "path": str(data_dir.absolute())
            }
        except Exception as e:
            logger.error(f"Storage check failed: {e}")
            return {
                "status": "unhealthy",
                "writable": False,
                "error": str(e)
            }

    def _check_logs(self) -> Dict[str, Any]:
        """Check if logs directory is accessible."""
        logs_dir = Path("logs")

        try:
            logs_dir.mkdir(exist_ok=True)

            # Try to write a test file
            test_file = logs_dir / ".health_check"
            test_file.write_text("OK")
            test_file.unlink()

            return {
                "status": "healthy",
                "writable": True,
                "path": str(logs_dir.absolute())
            }
        except Exception as e:
            logger.error(f"Logs check failed: {e}")
            return {
                "status": "unhealthy",
                "writable": False,
                "error": str(e)
            }

    def _check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space."""
        try:
            import shutil

            total, used, free = shutil.disk_usage("/")

            # Convert to GB
            total_gb = total / (1024**3)
            used_gb = used / (1024**3)
            free_gb = free / (1024**3)
            usage_percent = (used / total) * 100

            # Warn if less than 1GB free or more than 90% used
            status = "healthy"
            if free_gb < 1 or usage_percent > 90:
                status = "warning"
                logger.warning(f"Low disk space: {free_gb:.2f}GB free ({usage_percent:.1f}% used)")

            return {
                "status": status,
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "usage_percent": round(usage_percent, 1)
            }
        except Exception as e:
            logger.error(f"Disk space check failed: {e}")
            return {
                "status": "unknown",
                "error": str(e)
            }

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get system metrics and statistics.

        Returns:
            Dictionary containing system metrics.
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "uptime_formatted": self._format_uptime()
        }

        # Add file counts if directories exist
        if Path("data").exists():
            metrics["data_files"] = len(list(Path("data").glob("*.json")))

        if Path("logs").exists():
            metrics["log_files"] = len(list(Path("logs").glob("*.log")))

        if Path("backups").exists():
            metrics["backup_files"] = len(list(Path("backups").glob("*.tar.gz")))

        return metrics

    def _format_uptime(self) -> str:
        """Format uptime in a human-readable format."""
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def is_healthy(self) -> bool:
        """
        Quick health check.

        Returns:
            True if the system is healthy, False otherwise.
        """
        health = self.check_health()
        return health["status"] == "healthy"
