# AGENT CONTEXT VALIDATION PROTOCOL

When you (the agent) receive ANY request, execute this validation BEFORE taking action:

## Step 1: Identify Project Context
- Check: Does this workspace have a `.project-identity.txt` file?
- Read it. What is `PROJECT_NAME`, `PROJECT_TYPE`, `SCOPE`?
- What are the `CRITICAL RULE FOR AGENTS`?

## Step 2: Validate Request Alignment
Ask yourself: Does the user's request match this project's scope?

### RED FLAGS (request is for DIFFERENT project):
- Mentions DRY_RUN, LIVE_TRADING flags → Likely KuCoin bot
- Mentions lag_logger, lag_metrics, latency → Likely KuCoin bot
- Mentions symbol_gater, gating decisions → Likely KuCoin bot
- Mentions early_dd_breaker, drawdown halt → Likely KuCoin bot
- Mentions KuCoin API, margin trading, borrow rates → Likely KuCoin bot
- Mentions "2-week project", "5 agents", "instrumentation" → Likely KuCoin bot
- Workspace path is NOT C:\workspace\ → Different project

### GREEN FLAGS (request is for THIS project):
- Mentions SOL/USDT, BTC/USDT trading
- Mentions "soak test", "open position", "lifecycle"
- Mentions orchestrator, risk management, paper trading
- Mentions daily risk reset, status snapshot
- Workspace is C:\workspace\

## Step 3: If Context Mismatch Detected
STOP. Do not proceed. Output:

```
⚠️ CONTEXT MISMATCH DETECTED

This workspace is: [PROJECT_NAME from .project-identity.txt]
Your request appears to reference: [Different Project Name]

Before I proceed, please clarify:
1. Which project do you want me to work on?
2. Should I open a DIFFERENT VS Code window for that project?
3. Do you want me to switch projects, or stay focused on [CURRENT PROJECT]?
```

Then WAIT for user clarification.

## Step 4: If Context Matches
Proceed normally with the request.

## Step 5: On File Operations
Before editing ANY file:
- Verify the file is in the current project workspace
- Verify no git changes are in progress on other repos
- If in doubt, ask

## Step 6: Terminal Commands
ONLY use terminal for:
- Running code in the current workspace
- Checking git status in the current workspace
- Reading logs in the current workspace

NEVER use terminal to:
- Scan C:\ drive looking for other projects
- cd into directories outside the workspace
- Probe other repos' code

---

## Implementation for Current Agent (GitHub Copilot)

At the start of each new conversation or major request, log:

```
[AGENT VALIDATION] 
Project: Multi-Agent Orchestrator Trading Bot (C:\workspace\)
Status: Context validated ✓
Ready to proceed.
```

If at ANY point a request seems misaligned, invoke the CONTEXT MISMATCH protocol above.
