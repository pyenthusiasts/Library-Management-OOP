# Production Deployment Guide

This guide covers deploying the Library Management System in a production environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Docker Deployment](#docker-deployment)
4. [Systemd Service](#systemd-service)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [Backup Strategy](#backup-strategy)
7. [Security Best Practices](#security-best-practices)
8. [Performance Tuning](#performance-tuning)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (for containerized deployment)
- Sufficient disk space (recommended: 10GB+)
- Linux/Unix environment (Ubuntu 20.04+ recommended)

## Environment Configuration

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with production values:

```bash
# Library Settings
LIBRARY_NAME="Production Library"
MAX_BOOKS_PER_MEMBER=5
LOAN_PERIOD_DAYS=14
LATE_FEE_PER_DAY=1.00

# Storage Configuration
STORAGE_PATH=data/library_data.json
STORAGE_TYPE=json

# Logging Configuration
LOG_LEVEL=INFO
LOG_DIR=logs
ENABLE_AUDIT_LOG=true

# Application Settings
ENV=production
DEBUG=false

# Security (IMPORTANT: Change in production!)
SECRET_KEY=<generate-strong-random-key>
```

### 3. Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Docker Deployment

### Quick Start

```bash
# Build and start containers
make docker-build
make docker-up

# View logs
make docker-logs

# Stop containers
make docker-down
```

### Manual Docker Commands

```bash
# Build image
docker build -t library-management-system:latest .

# Run container
docker run -d \
  --name library-system \
  -v library-data:/app/data \
  -v library-logs:/app/logs \
  --env-file .env \
  library-management-system:latest

# View logs
docker logs -f library-system

# Stop container
docker stop library-system
docker rm library-system
```

### Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# Scale services (if needed)
docker-compose up -d --scale library-system=3

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

## Systemd Service

For non-containerized deployments, create a systemd service.

### 1. Create Service File

Create `/etc/systemd/system/library-system.service`:

```ini
[Unit]
Description=Library Management System
After=network.target

[Service]
Type=simple
User=library
Group=library
WorkingDirectory=/opt/library-system
Environment="PATH=/opt/library-system/venv/bin"
ExecStart=/opt/library-system/venv/bin/library-cli
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/library-system/data /opt/library-system/logs

[Install]
WantedBy=multi-user.target
```

### 2. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable library-system

# Start service
sudo systemctl start library-system

# Check status
sudo systemctl status library-system

# View logs
sudo journalctl -u library-system -f
```

## Monitoring and Logging

### Log Files

Logs are stored in the `logs/` directory:

- `library_system.log` - Main application log (INFO and above)
- `library_errors.log` - Error log (ERROR and above)
- `library_audit.log` - Audit trail of all operations
- `audit_trail.jsonl` - Machine-readable audit log (JSON Lines)

### Log Rotation

Logs automatically rotate when they reach 10MB, keeping 5 backups for system logs and 10 for audit logs.

### Health Checks

```python
from library_system.services.health_service import HealthService

health = HealthService()

# Perform health check
status = health.check_health()
print(status)

# Quick check
is_healthy = health.is_healthy()

# Get metrics
metrics = health.get_metrics()
```

### Monitoring Script

Create a monitoring script:

```bash
#!/bin/bash
# monitor.sh

while true; do
    python3 -c "
from library_system.services.health_service import HealthService
health = HealthService()
if not health.is_healthy():
    print('ALERT: System unhealthy!')
    exit(1)
print('System healthy')
"
    sleep 300  # Check every 5 minutes
done
```

## Backup Strategy

### Automatic Backups

#### Cron Job

Add to crontab (`crontab -e`):

```bash
# Daily backup at 2 AM
0 2 * * * cd /opt/library-system && make backup

# Weekly backup with logs (Sunday 3 AM)
0 3 * * 0 cd /opt/library-system && python3 -c "from library_system.services import BackupService; BackupService().create_backup(include_logs=True)"
```

#### Systemd Timer

Create `/etc/systemd/system/library-backup.timer`:

```ini
[Unit]
Description=Library System Daily Backup
Requires=library-backup.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

Create `/etc/systemd/system/library-backup.service`:

```ini
[Unit]
Description=Library System Backup

[Service]
Type=oneshot
User=library
WorkingDirectory=/opt/library-system
ExecStart=/opt/library-system/venv/bin/python3 -c "from library_system.services import BackupService; BackupService().create_scheduled_backup()"
```

Enable:

```bash
sudo systemctl enable library-backup.timer
sudo systemctl start library-backup.timer
```

### Manual Backup

```bash
# Using Makefile
make backup

# Using Python
python3 -c "from library_system.services import BackupService; BackupService().create_backup()"
```

### Restore from Backup

```bash
# List backups
ls -lh backups/

# Restore
python3 -c "
from pathlib import Path
from library_system.services import BackupService
bs = BackupService()
bs.restore_backup(Path('backups/library_backup_20250113_020000.tar.gz'))
"
```

### Off-site Backup

```bash
# Sync to remote server
rsync -avz backups/ user@backup-server:/backups/library-system/

# Or use cloud storage (AWS S3 example)
aws s3 sync backups/ s3://my-bucket/library-backups/
```

## Security Best Practices

### 1. File Permissions

```bash
# Set proper ownership
sudo chown -R library:library /opt/library-system

# Set directory permissions
find /opt/library-system -type d -exec chmod 750 {} \;

# Set file permissions
find /opt/library-system -type f -exec chmod 640 {} \;

# Make scripts executable
chmod 750 /opt/library-system/scripts/*.py
```

### 2. Network Security

- Run the application on a private network
- Use firewall rules to restrict access
- Implement reverse proxy with SSL/TLS

### 3. Data Encryption

```bash
# Encrypt backup files
gpg --symmetric --cipher-algo AES256 backups/library_backup_latest.tar.gz

# Decrypt when needed
gpg --decrypt backups/library_backup_latest.tar.gz.gpg > restored_backup.tar.gz
```

### 4. Access Control

- Use strong authentication for system access
- Implement role-based access control (RBAC)
- Regular security audits

### 5. Audit Logging

All operations are logged to `logs/audit_trail.jsonl`. Review regularly:

```bash
# View recent audit events
tail -f logs/audit_trail.jsonl | jq .

# Search for specific operations
grep "BORROW_BOOK" logs/audit_trail.jsonl | jq .

# Failed operations
grep '"success":false' logs/audit_trail.jsonl | jq .
```

## Performance Tuning

### 1. Optimize JSON Storage

For large libraries, consider switching to SQLite:

```bash
# In .env
STORAGE_TYPE=sqlite
DATABASE_URL=sqlite:///data/library.db
```

### 2. Log Level

In production, use INFO or WARNING level:

```bash
# In .env
LOG_LEVEL=INFO
```

### 3. Disk I/O

- Use SSD storage for better performance
- Mount `data/` and `logs/` on separate volumes if possible

### 4. Memory Management

Monitor memory usage:

```bash
# Check Python process memory
ps aux | grep library-cli

# Monitor with htop
htop -p $(pgrep -f library-cli)
```

## Troubleshooting

### Common Issues

#### 1. Permission Denied

```bash
# Fix file permissions
sudo chown -R library:library /opt/library-system
chmod -R 755 /opt/library-system
```

#### 2. Storage Not Writable

```bash
# Check directory permissions
ls -ld data logs backups

# Create if missing
mkdir -p data logs backups
chmod 755 data logs backups
```

#### 3. Corrupt Data File

```bash
# Restore from backup
make restore

# Or manually
cp backups/library_backup_latest.tar.gz .
tar -xzf library_backup_latest.tar.gz
cp library_data.json data/
```

#### 4. High Memory Usage

```bash
# Restart service
sudo systemctl restart library-system

# Or Docker
docker-compose restart library-system
```

### Debug Mode

Enable debug logging temporarily:

```bash
# In .env
LOG_LEVEL=DEBUG
DEBUG=true

# Restart service
sudo systemctl restart library-system
```

### Health Check

```bash
# Quick health check
python3 -c "
from library_system.services.health_service import HealthService
import json
health = HealthService()
print(json.dumps(health.check_health(), indent=2))
"
```

## Maintenance

### Regular Tasks

**Daily:**
- Monitor logs for errors
- Check disk space
- Verify backups completed

**Weekly:**
- Review audit logs
- Check system health metrics
- Test backup restoration

**Monthly:**
- Update dependencies
- Security patches
- Performance analysis
- Clean old logs and backups

### Update Procedure

```bash
# 1. Create backup
make backup

# 2. Pull latest code
git pull origin main

# 3. Update dependencies
pip install --upgrade -e ".[dev]"

# 4. Run migrations if needed
make migrate

# 5. Run tests
make test

# 6. Restart service
sudo systemctl restart library-system
```

## Support and Monitoring

### Metrics to Track

- Storage file size growth
- Number of operations per day
- Error rate
- Response times
- Disk space usage
- Backup success rate

### Alerting

Set up alerts for:
- System health failures
- Disk space < 10%
- Failed backups
- High error rates
- Service downtime

---

For additional help, see:
- [API Documentation](API.md)
- [README](../README.md)
- [GitHub Issues](https://github.com/pyenthusiasts/Library-Management-OOP/issues)
