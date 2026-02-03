#!/usr/bin/env powershell
<#
AGENT CONTEXT SANITY CHECK
Run this before asking an agent to do work on either project
#>

Write-Host "======================================"
Write-Host "AGENT CONTEXT SANITY CHECK"
Write-Host "=====================================" -ForegroundColor Green

$projects = @(
    @{ Name = "Orchestrator Bot"; Path = "C:\workspace"; Identity = ".project-identity.txt" },
    @{ Name = "KuCoin Margin Bot"; Path = "C:\bot_backups\kucoin-margin-bot_copy_20260128_051315"; Identity = ".project-identity.txt" }
)

foreach ($project in $projects) {
    Write-Host "`n[CHECK] $($project.Name)" -ForegroundColor Cyan
    Write-Host "  Path: $($project.Path)"
    
    if (Test-Path $project.Path) {
        Write-Host "  Status: EXISTS ✓" -ForegroundColor Green
        
        # Check for .project-identity.txt
        if (Test-Path "$($project.Path)/$($project.Identity)") {
            Write-Host "  Identity file: FOUND ✓" -ForegroundColor Green
        } else {
            Write-Host "  Identity file: MISSING ✗" -ForegroundColor Yellow
        }
        
        # Check git status
        Push-Location $project.Path
        $gitStatus = git status --short 2>&1
        if ($LASTEXITCODE -eq 0) {
            $modifiedCount = ($gitStatus | Measure-Object).Count
            Write-Host "  Git repo: YES" -ForegroundColor Green
            Write-Host "  Modified files: $modifiedCount"
            if ($modifiedCount -gt 0) {
                Write-Host "  WARNING: Uncommitted changes in this project!" -ForegroundColor Yellow
                $gitStatus | ForEach-Object { Write-Host "    $_" }
            }
        } else {
            Write-Host "  Git repo: NO (not a git repo)" -ForegroundColor Yellow
        }
        Pop-Location
    } else {
        Write-Host "  Status: NOT FOUND ✗" -ForegroundColor Red
    }
}

Write-Host "`n======================================"
Write-Host "AGENT: Before accepting a request, ask:"
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "1. Which project is this for?"
Write-Host "2. Does the request mention project-specific keywords?"
Write-Host "3. Should you open a separate VS Code window?"
