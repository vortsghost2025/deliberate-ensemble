# ORCHESTRATOR BOT - DOCKER DEPLOYMENT GUIDE

## Quick Start (Local Docker)

### 1. Build the Docker image

```powershell
cd C:\workspace
docker build -t orchestrator-trading-bot:latest .
```

**Output**: Creates image `orchestrator-trading-bot:latest` (~500MB, includes Python 3.11 + dependencies)

---

### 2. Run with docker-compose (recommended)

```powershell
cd C:\workspace
docker-compose up -d
```

**What this does:**
- Builds the image if not present
- Starts container: `orchestrator-trading-bot`
- Mounts `./logs` directory for persistent log files
- Sets up health checks (checks every 60s)
- Auto-restarts on failure

**View logs:**
```powershell
docker-compose logs -f orchestrator-bot
# or
Get-Content C:\workspace\logs\trading_bot.log -Tail 50 -Wait
```

**Stop the bot:**
```powershell
docker-compose down
```

---

### 3. Run with plain Docker (if not using compose)

```powershell
docker run -d \
  --name orchestrator-trading-bot \
  -v C:\workspace\logs:/app/logs \
  -v C:\workspace\config:/app/config \
  --restart unless-stopped \
  orchestrator-trading-bot:latest
```

---

## Docker Commands

### Check if container is running
```powershell
docker ps | Select-String orchestrator
```

### View real-time logs
```powershell
docker logs -f orchestrator-trading-bot
```

### Stop the container
```powershell
docker stop orchestrator-trading-bot
```

### Restart the container
```powershell
docker restart orchestrator-trading-bot
```

### Remove the container
```powershell
docker rm orchestrator-trading-bot
```

### Remove the image
```powershell
docker rmi orchestrator-trading-bot:latest
```

---

## Deployment to Oracle Cloud VM

### Prerequisites
- Oracle Cloud VM with Docker installed
- SSH access to the VM
- SCP or equivalent for file transfer

### Steps

1. **Transfer project to Oracle VM**
```powershell
# On your local machine, copy to Oracle VM
scp -r C:\workspace\* username@oracle-vm-ip:/home/username/orchestrator-bot/
```

2. **SSH into Oracle VM**
```powershell
ssh username@oracle-vm-ip
cd /home/username/orchestrator-bot
```

3. **Build Docker image on Oracle VM**
```bash
docker build -t orchestrator-trading-bot:latest .
```

4. **Run container on Oracle VM**
```bash
docker-compose up -d
# or
docker run -d \
  --name orchestrator-trading-bot \
  -v ./logs:/app/logs \
  --restart unless-stopped \
  orchestrator-trading-bot:latest
```

5. **Verify it's running**
```bash
docker ps | grep orchestrator
docker logs orchestrator-trading-bot
```

---

## Persistent Logs

**Local:** Logs are saved to `C:\workspace\logs\trading_bot.log`  
**Docker:** Logs are also inside the container at `/app/logs/`

Both stay synchronized via the volume mount in docker-compose.yml

---

## Health Checks

The container includes a health check that runs every 60 seconds:
- If the bot crashes, the container will auto-restart
- View health status: `docker ps`

---

## Updating the Bot

If you make code changes:

1. **Rebuild the image**
```powershell
docker-compose down
docker build -t orchestrator-trading-bot:latest .
docker-compose up -d
```

2. **Or use one command**
```powershell
docker-compose up -d --build
```

---

## Troubleshooting

### Container exits immediately
```powershell
docker logs orchestrator-trading-bot  # Check error messages
```

### Port conflicts (if you add a web API later)
```powershell
docker ps  # See all containers
docker port orchestrator-trading-bot  # See port mappings
```

### Out of disk space
```powershell
docker system prune -a  # Remove unused images/containers
```

---

## Production Considerations (Future)

- Add environment variables for API keys (use `.env` file)
- Set resource limits: `--memory 512m --cpus 1`
- Use persistent volumes for database
- Add monitoring/alerting (Prometheus, Grafana)
- Use Docker secrets for sensitive configs
