# MULTI-PROJECT SEPARATION CHECKLIST

## Current Situation
You have (at least) 2 active trading bot projects:

1. **Orchestrator Bot** (NEW - built 2026-02-02 by collab AI)
   - Path: `C:\workspace\`
   - Status: Soak testing, active
   - Agent: GitHub Copilot (focused, single-project)
   
2. **KuCoin Margin Bot** (LEGACY - started 2 weeks ago, 8 agents)
   - Path: `C:\bot_backups\kucoin-margin-bot_copy_20260128_051315` (and others)
   - Status: DRY_RUN testing
   - Features: lag_logger, symbol_gater, early_dd_breaker (not yet integrated)
   - Agent: ??? (not scoped in this session)

## Risk of Confusion

If you don't clearly separate these, an agent could:
1. Get a request about "DRY_RUN instrumentation"
2. See the orchestrator bot is running
3. Assume that's where the work goes
4. Start editing orchestrator code to add lag_logger (WRONG)
5. Break the working orchestrator bot

## Solution: Project Boundaries

### For Orchestrator Bot (THIS SESSION'S FOCUS)

**Workspace**: `C:\workspace\`  
**Identity File**: `.project-identity.txt` ✓ (created)  
**Agent Protocol**: `AGENT_OPERATIONAL_PROTOCOL.md` ✓ (created)  
**Context Check**: `AGENT_CONTEXT_CHECK.ps1` ✓ (created)  
**VS Code Window**: Use THIS one for orchestrator work only

### For KuCoin Bot (FUTURE SESSIONS)

**Before starting work on KuCoin bot:**
1. Create a NEW VS Code window
2. Open the KuCoin bot folder as the workspace
3. Create `.project-identity.txt` in that folder:

```text
PROJECT_NAME: KuCoin Margin Bot (Fortress Ensemble)
PROJECT_TYPE: Live + DRY_RUN Trading with Risk Instrumentation
VERSION: 2.0-dryrun-instrumented
CREATED: 2026-01-23 (started by user, enhanced with DRY_RUN)
PURPOSE: 2-week DRY_RUN validation with lag metrics, gating, early DD

SCOPE:
- Multiple agents (historical, now consolidating)
- DRY_RUN mode for safe testing
- LIVE_TRADING mode (gated, with circuit breakers)
- KuCoin Futures + Spot API
- Margin trading with borrow rates

KEY FEATURES:
- lag_metrics_logger.py (signal-to-entry latency tracking)
- symbol_gating_manager.py (trade approval logic)
- early_dd_breaker.py (portfolio drawdown halt)
- generate_dryrun_report.py (validation reporting)

CRITICAL RULE FOR AGENTS:
If a request mentions:
  - SOL/USDT, BTC/USDT, orchestrator, risk_manager
  - Paper trading, daily risk reset
  - Multi-agent orchestration
THEN: This is NOT for this project. Ask user for clarification.
```

4. Create `AGENT_OPERATIONAL_PROTOCOL.md` for the KuCoin bot scope
5. Instruct the agent: "Focus on KuCoin bot only in this window"

## How to Prevent Cross-Project Contamination

### Rule 1: One Window = One Project
- Orchestrator bot → THIS VS Code window only
- KuCoin bot → SEPARATE VS Code window
- Never work on both simultaneously in one session

### Rule 2: Agent Validation at Session Start
Before giving an agent any work, say:
```
"I'm working on [PROJECT NAME]. Here's the .project-identity.txt file.
Please read it and confirm you understand the project scope before proceeding."
```

### Rule 3: Explicit Context Switching
If you switch projects mid-session:
1. Close the current VS Code window or switch workspace
2. Open a NEW window with the other project
3. Explicitly tell the agent: "New project: [NAME]. Read the identity file."

### Rule 4: No Cross-Project Navigation
Instruct agents: "Do NOT use terminal to explore other projects."  
If an agent says "I found the other project at C:\...", say:
```
"Stop. That's a different project. If you need to work on it,
I'll open a separate window for it. For now, stay in this workspace only."
```

## Quick Identification Cheat Sheet

| Signal | Project |
|--------|---------|
| "SOL/USDT, BTC/USDT" | Orchestrator |
| "Paper trading" | Orchestrator |
| "Orchestrator, daily risk reset" | Orchestrator |
| "DRY_RUN, LIVE_TRADING" | KuCoin |
| "lag_logger, gating" | KuCoin |
| "early_dd, drawdown" | KuCoin |
| "KuCoin API, margin" | KuCoin |
| "2-week project, 8 agents" | KuCoin |

---

## Action Items

- [ ] Orchestrator bot has `.project-identity.txt` ✓
- [ ] Orchestrator bot has `AGENT_OPERATIONAL_PROTOCOL.md` ✓
- [ ] Orchestrator bot has `AGENT_CONTEXT_CHECK.ps1` ✓
- [ ] When starting KuCoin bot work: Create new VS Code window
- [ ] Create `.project-identity.txt` for KuCoin bot
- [ ] Create `AGENT_OPERATIONAL_PROTOCOL.md` for KuCoin bot
- [ ] Before every agent request: Verify project context

---

## Going Forward

**This Session**: Orchestrator bot only. All requests assume that scope.  
**Next Time You Work on KuCoin**: New window, new identity file, explicit context.  
**Result**: No more accidental cross-project contamination.
