# ORCHESTRATOR BOT - ORACLE CLOUD DEPLOYMENT GUIDE

## Overview

This guide walks through deploying the orchestrator bot on an Oracle Cloud VM for always-on, production-grade trading.

---

## Architecture

```
Your Local Machine (Development)
    ↓
Docker Container Built Locally
    ↓
Transfer to Oracle Cloud
    ↓
Oracle Linux VM (always-on)
    ↓
Docker Container Running 24/7
    ↓
Logs → Persistent Storage
Trade Data → Local State
```

---

## Step 1: Prepare Oracle Cloud VM

### 1.1 Create or use existing VM

**Required specs:**
- **OS**: Oracle Linux 8+ or Ubuntu 20.04+
- **CPU**: 2 cores minimum
- **RAM**: 2-4 GB
- **Disk**: 20 GB (for logs, configs, data)
- **Network**: Allow outbound HTTP/HTTPS (for CoinGecko API)

### 1.2 SSH into your VM

```bash
ssh -i /path/to/private_key username@your-oracle-vm-ip
```

### 1.3 Install Docker (if not already installed)

**For Oracle Linux 8:**
```bash
sudo dnf install -y docker-engine
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

**For Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

**Verify Docker is running:**
```bash
docker --version
docker ps
```

---

## Step 2: Transfer Project to Oracle VM

### Option A: Using SCP (recommended)

**From your local machine:**
```powershell
# Copy entire project folder
scp -i C:\path\to\oracle_key -r C:\workspace\* username@oracle-vm-ip:/home/username/orchestrator-bot/

# Or copy specific files
scp -i C:\path\to\oracle_key C:\workspace\main.py username@oracle-vm-ip:/home/username/orchestrator-bot/
scp -i C:\path\to\oracle_key C:\workspace\Dockerfile username@oracle-vm-ip:/home/username/orchestrator-bot/
scp -i C:\path\to\oracle_key C:\workspace\docker-compose.yml username@oracle-vm-ip:/home/username/orchestrator-bot/
```

### Option B: Using Git

**On the Oracle VM:**
```bash
git clone https://your-repo-url.git orchestrator-bot
cd orchestrator-bot
```

---

## Step 3: Build Docker Image on Oracle VM

```bash
cd /home/username/orchestrator-bot

# Build the image
docker build -t orchestrator-trading-bot:latest .

# Verify it built successfully
docker images | grep orchestrator
```

---

## Step 4: Run the Bot in Docker

### Option A: Using docker-compose (recommended)

```bash
docker-compose up -d
```

### Option B: Using plain docker

```bash
docker run -d \
  --name orchestrator-trading-bot \
  -v /home/username/orchestrator-bot/logs:/app/logs \
  --restart unless-stopped \
  orchestrator-trading-bot:latest
```

### Verify it's running

```bash
docker ps | grep orchestrator
docker logs orchestrator-trading-bot
```

---

## Step 5: Monitor the Bot

### View logs in real-time

```bash
docker logs -f orchestrator-trading-bot
# or
tail -f /home/username/orchestrator-bot/logs/trading_bot.log
```

### Check status

```bash
# View live metrics
docker stats orchestrator-trading-bot

# Check health
docker ps orchestrator-trading-bot
```

### Connect to logs remotely

**From your local machine:**
```powershell
scp -i C:\path\to\oracle_key -r username@oracle-vm-ip:/home/username/orchestrator-bot/logs/ C:\workspace\remote-logs\
```

---

## Step 6: Set Up Persistent Storage

### Ensure logs persist across restarts

The docker-compose.yml already mounts:
- `./logs:/app/logs` → Logs saved locally on VM

**Backup logs periodically:**
```bash
# On Oracle VM
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

---

## Step 7: Configure Auto-Restart

### With docker-compose

The `--restart unless-stopped` is already in docker-compose.yml, so:
- If container crashes, Docker auto-restarts it
- If VM reboots, the service starts automatically

### Verify auto-restart is working

```bash
# Stop the container
docker stop orchestrator-trading-bot

# Wait 5 seconds, check if it restarted
sleep 5
docker ps | grep orchestrator
```

---

## Ongoing Operations

### Check bot status from your local machine

```powershell
# SSH into Oracle VM and check
ssh -i C:\path\to\oracle_key username@oracle-vm-ip "docker logs orchestrator-trading-bot | tail -20"

# Or run the status command if accessible
ssh -i C:\path\to\oracle_key username@oracle-vm-ip "cd /home/username/orchestrator-bot && python main.py status"
```

### Update bot code

```bash
# On Oracle VM
cd /home/username/orchestrator-bot

# Pull latest from git (if using git)
git pull

# Rebuild and restart
docker-compose up -d --build
```

### View resource usage

```bash
docker stats orchestrator-trading-bot
```

---

## Troubleshooting

### Container won't start

```bash
docker logs orchestrator-trading-bot  # Check error messages
docker rm orchestrator-trading-bot    # Remove container
docker build -t orchestrator-trading-bot:latest .  # Rebuild
docker-compose up -d  # Start again
```

### Out of disk space

```bash
# Check disk usage
df -h

# Clean up old logs
rm orchestrator-bot/logs/trading_bot.log.*

# Docker cleanup
docker system prune -a
```

### Network/API connectivity

```bash
# Test CoinGecko API access from Oracle VM
curl -s https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd | head

# If blocked, may need to configure firewall
```

### Need to rebuild completely

```bash
docker-compose down
docker rmi orchestrator-trading-bot:latest
docker build -t orchestrator-trading-bot:latest .
docker-compose up -d
```

---

## Security Best Practices

### Protect your SSH key

```bash
chmod 600 /path/to/oracle_key
```

### Use environment variables for sensitive data

Create `.env` file in orchestrator-bot folder:
```
COINGECKO_API_KEY=your_key_here
```

Update docker-compose.yml to load it:
```yaml
services:
  orchestrator-bot:
    env_file: .env
```

### Restrict firewall

```bash
# Only allow SSH (22) and your management ports
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload
```

---

## Performance Tuning

### Limit container resources (optional)

Edit docker-compose.yml:
```yaml
services:
  orchestrator-bot:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

### Enable log rotation

Add to docker-compose.yml:
```yaml
services:
  orchestrator-bot:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Reference Commands

```bash
# Start bot
docker-compose up -d

# Stop bot
docker-compose down

# View logs
docker logs -f orchestrator-trading-bot

# SSH from local
ssh -i key.pem username@oracle-vm-ip

# Copy files from local to Oracle
scp -i key.pem file.txt username@oracle-vm-ip:/home/username/

# Copy files from Oracle to local
scp -i key.pem username@oracle-vm-ip:/home/username/file.txt ./
```

---

## Support

If issues arise:
1. Check logs: `docker logs orchestrator-trading-bot`
2. Check disk space: `df -h`
3. Verify Docker: `docker ps`
4. Rebuild: `docker-compose up -d --build`
