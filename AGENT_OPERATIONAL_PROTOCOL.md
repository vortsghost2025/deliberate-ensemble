# AGENT OPERATIONAL PROTOCOL
## Multi-Agent Orchestrator Trading Bot
**Last Updated**: 2026-02-03  
**Project**: C:\workspace\  
**Built By**: Collab AI (LMArena) + GitHub Copilot

---

## MISSION STATEMENT
This agent is responsible for ONE project only:
- **Multi-Agent Orchestrator Trading Bot** (paper trading, risk management, soak testing)
- NOT responsible for KuCoin margin bot, legacy bots, or other projects
- NOT responsible for DRY_RUN instrumentation, lag metrics, or gating logic

---

## CONTEXT VALIDATION (DO THIS FIRST)

### Before accepting ANY request:

1. **Read `.project-identity.txt`** in the workspace root
2. **Classify the request**:
   - Is it about SOL/USDT, BTC/USDT, orchestration, risk, paper trading? → **MINE**
   - Is it about DRY_RUN, LIVE_TRADING, KuCoin API, lag_logger, gating, early_dd? → **NOT MINE**
   - Is it ambiguous? → **ASK FOR CLARIFICATION**

3. **If NOT MINE**: Output this and STOP:
```
⚠️ CONTEXT MISMATCH

This request references features/components NOT in this project:
[List what you detected]

You have asked me to work on: [Inferred Project Name]
But I am currently scoped to: Multi-Agent Orchestrator Trading Bot

Please clarify:
- Should I open a NEW VS Code window for [Other Project]?
- Or is this actually for the orchestrator bot?

I will NOT proceed until you confirm.
```

4. **If MINE**: Log and proceed:
```
✓ Context validated: Multi-Agent Orchestrator Bot
✓ Scope: C:\workspace\
✓ Proceeding with request
```

---

## FILE EDITING GUARDRAILS

### DO:
- Edit files in `C:\workspace\` and subdirectories
- Edit main.py, agents/, config files
- Run code via terminal in this workspace
- Check git status in this workspace

### DO NOT:
- Use terminal to scan C:\ drive
- `cd` into `C:\kucoin-margin-bot-test`, `C:\TradingBot`, `C:\Users\seand\OneDrive\Desktop\Testingbot`, etc.
- Probe other projects' code to "find" components
- Edit state files in other projects
- Assume a shell script with a similar name is "the same project"

### If you find yourself thinking:
- "Let me check the other bot to understand the pattern"
- "I'll just scan a few files from the KuCoin repo"
- "Maybe I can integrate this feature from the backup"

**STOP.** That's a sign the request is out of scope. Invoke the context mismatch protocol above.

---

## TERMINAL USAGE

### Safe terminal operations:
```powershell
python C:\workspace\main.py          # Run the bot
python C:\workspace\main.py status   # Check status
Get-Content C:\workspace\logs\*.log  # Read logs
```

### Dangerous terminal operations (DO NOT DO):
```powershell
Get-ChildItem C:\ -Recurse           # Scanning entire drive
cd C:\some\other\project             # Changing out of workspace
Get-Content C:\bot_backups\...       # Reading other projects
```

---

## CURRENT MISSION STATUS

**Active**: Soak test of SOL/USDT trading with open positions  
**State**: Trade #1 open @ $101.55, monitoring for SL/TP exit  
**Role**: Run cycles, collect data, report on system health  
**Autonomy**: YES - can run multiple cycles without asking  

### What the agent should do:
1. Run `python C:\workspace\main.py` periodically (or on user request)
2. Check `python C:\workspace\main.py status` to verify health
3. Report back: trades opened, PnL, positions, agent state
4. Watch for errors and surface them
5. Collect logs and highlight patterns

### What the agent should NOT do:
1. Try to "improve" the bot by integrating other projects' logic
2. Wander looking for "related" files in other directories
3. Make architectural changes without user confirmation
4. Edit configuration based on guesses about "what might work better"

---

## IF YOU GET CONFUSED

Print this and restart the conversation:

```
PROJECT CHECK:
- Name: Multi-Agent Orchestrator Trading Bot
- Path: C:\workspace\
- Status: Soak testing, one open position
- Agent: GitHub Copilot (single agent, no coordination)

If request references something NOT listed above, ASK.
```

---

## QUESTIONS TO ASK BEFORE PROCEEDING

1. "Is this request for the orchestrator bot or a different project?"
2. "Should I open a separate VS Code window for that other project?"
3. "Does this file I'm about to edit belong to C:\workspace\?"
4. "Have I read `.project-identity.txt` to validate context?"
5. "Am I about to use terminal to scan outside the workspace?"

**If you can't confidently answer YES to all of these, ASK THE USER.**
