#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Monitor the paper trading soak test in real-time
.DESCRIPTION
    Displays cycle count, error count, and live logs from the orchestrator paper trading soak
.USAGE
    .\monitor_paper_soak.ps1
#>

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      ORCHESTRATOR PAPER TRADING SOAK TEST MONITOR             ║" -ForegroundColor Cyan
Write-Host "║              Real-time Performance Tracking                   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$container = "orchestrator-paper-soak"

# Check if container exists
if (-not (docker ps -a --filter "name=$container" --format "{{.Names}}" | Where-Object {$_ -eq $container})) {
    Write-Host "❌ Container '$container' not found. Start with:" -ForegroundColor Red
    Write-Host "   docker run -d --name $container orchestrator-bot:latest"
    exit 1
}

Write-Host "Container Status:" -ForegroundColor Yellow
docker ps --filter "name=$container" --format "  {{.Names}}: {{.Status}}"
Write-Host ""

# Display last 30 lines and follow
Write-Host "Live Logs (Ctrl+C to exit):" -ForegroundColor Yellow
Write-Host "──────────────────────────────────────────────────────────────────" -ForegroundColor Gray
docker logs --tail 30 -f $container 2>&1 | ForEach-Object {
    if ($_ -match "Starting Trading Cycle") {
        Write-Host $_ -ForegroundColor Green
    }
    elseif ($_ -match "ERROR|error|429") {
        Write-Host $_ -ForegroundColor Red
    }
    elseif ($_ -match "COINGECKO|backoff") {
        Write-Host $_ -ForegroundColor Yellow
    }
    elseif ($_ -match "OK|success|approved") {
        Write-Host $_ -ForegroundColor Green
    }
    else {
        Write-Host $_
    }
}
