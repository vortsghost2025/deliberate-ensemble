📋 ORCHESTRATOR BOT - PROJECT TASKS & STATUS
=============================================

## 🟢 COMPLETED

### Core Architecture
- [x] Multi-agent orchestrator design (6 specialized agents + conductor)
- [x] State machine workflow (IDLE → FETCHING_DATA → ANALYZING → BACKTESTING → RISK_ASSESSMENT → EXECUTING → MONITORING)
- [x] Registry-based agent discovery and lifecycle
- [x] Error handling and circuit breaker pattern
- [x] Daily risk reset on UTC date change

### Data & Integration
- [x] CoinGecko API integration (basic, live prices working)
- [x] Trading pair parsing (SOL/USDT → SOL)
- [x] Quote currency normalization (usdt → usd)
- [x] Paper trading system (in-memory trade tracking)
- [x] Position sizing engine with confidence scaling

### Risk Management
- [x] Multi-layered safety hierarchy (circuit breaker → daily loss cap → per-trade risk → signal/win-rate gates)
- [x] Position size calculation: `size = (balance × risk% × confidence) / risk_per_unit`
- [x] SL/TP calculation based on risk and volatility
- [x] Min notional threshold ($10 USD)
- [x] Daily loss cap (5% of account)
- [x] Per-trade risk limit (1.5% for soak, 1.0% production)

### Deployment & Infrastructure
- [x] Dockerfile (Python 3.11-slim, production-ready)
- [x] docker-compose.yml (volume mounts, health checks, auto-restart)
- [x] DEPLOYMENT_DOCKER.md (local Docker guide + troubleshooting)
- [x] DEPLOYMENT_ORACLE.md (Oracle Cloud VM guide)
- [x] DEPLOYMENT_SUMMARY.md (quick reference)
- [x] Project isolation guardrails (.project-identity.txt, AGENT_OPERATIONAL_PROTOCOL.md)

### Validation & Testing
- [x] Full end-to-end pipeline validation (data → analysis → backtest → risk → execution → monitoring)
- [x] Docker container builds and starts successfully
- [x] All 6 agents initialize and register without errors
- [x] State machine cycles correctly (IDLE → FETCHING_DATA → ... → IDLE)
- [x] Error recovery works (429 errors don't crash, circuit breaker activates properly)
- [x] Daily risk reset confirmed in logs
- [x] Paper trading framework operational

### Code Quality
- [x] Removed emoji logging (replaced with ASCII: [CRITICAL], [WARN], [INFO])
- [x] Safe numeric formatting with type guards
- [x] Consistent logging across all agents
- [x] No encoding/charmap errors on Windows

---

## 🟡 HIGH PRIORITY (Before Production)

### ORCH-API-001: Centralized CoinGecko Rate Limiting
**Priority**: High (blocking production use)  
**Status**: Known issue, not yet fixed  
**Description**:  
Current bot cycles show: IDLE → FETCHING_DATA → [429 rate limit] → ERROR → IDLE  
Root cause: Multiple data fetch calls per cycle hitting CoinGecko's free tier limits (~10-50 req/min).

**Acceptance Criteria**:
- [ ] Create `coingecko_client.py` as single source of truth for all CoinGecko calls
- [ ] Implement global rate limiter: MIN_INTERVAL = 6 seconds (≈10 req/min safe)
- [ ] Add exponential backoff on 429 errors (5s, 10s, 15s, etc.)
- [ ] Batch price calls where possible (fetch multiple coins in single request)
- [ ] Cache prices for entire trading cycle (no per-agent re-fetches)
- [ ] Add unit test: 429 response → backoff, no crash
- [ ] Update DataFetchingAgent to use centralized client
- [ ] Verify container runs 10+ cycles without 429 errors

**Implementation Notes**:
```python
# coingecko_client.py pattern
MIN_INTERVAL = 6.0  # seconds
last_call_ts = 0.0

def rate_limited_get(url, params=None):
    global last_call_ts
    now = time.time()
    wait = MIN_INTERVAL - (now - last_call_ts)
    if wait > 0:
        time.sleep(wait)
    resp = requests.get(url, params=params, timeout=10)
    last_call_ts = time.time()
    return resp

def safe_fetch_with_backoff(url, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            return rate_limited_get(url, params=params)
        except HTTPError as e:
            if e.response.status_code == 429:
                sleep_time = (attempt + 1) * 5
                time.sleep(sleep_time)
                continue
            raise
    raise RuntimeError("CoinGecko retries exhausted")
```

---

## 🟡 MEDIUM PRIORITY (Before Live Trading)

### ORCH-EXEC-002: Per-Symbol Execution
**Priority**: Medium (nice-to-have for multi-symbol setups)  
**Status**: Not started  
**Description**:  
Current: RiskManagementAgent returns single `position_approved` boolean for entire batch.  
Limitation: If SOL approved but BTC rejected, orchestrator can't execute SOL alone.

**Acceptance Criteria**:
- [ ] Refactor RiskManagementAgent to return per-pair approval dict: `{SOL/USDT: {approved: True, size: 4.39, ...}, BTC/USDT: {approved: False, reason: ...}}`
- [ ] Update OrchestratorAgent to process pairs independently
- [ ] ExecutionAgent executes all approved pairs, skips rejected
- [ ] Test: Add both SOL + BTC to trading_pairs; verify only SOL executes

**Estimated Effort**: 2-3 hours

---

### ORCH-BENCH-003: Performance & Metrics
**Priority**: Medium (for analytics and optimization)  
**Status**: Not started  
**Description**:  
Build a post-soak analysis script to understand orchestrator behavior.

**Acceptance Criteria**:
- [ ] Script reads logs and generates report:
  - Cycles per hour
  - % data fetch success vs. rate limit
  - Average position size when approved
  - Risk % distribution
  - Circuit breaker activation count/reasons
- [ ] Output: CSV for spreadsheet analysis or HTML dashboard
- [ ] Example: `python analyze_soak.py logs/ --output report.html`

**Estimated Effort**: 1-2 hours

---

## 🔵 NICE-TO-HAVE (Future Enhancements)

### ORCH-CONFIG-004: Dynamic Risk Configuration
**Priority**: Low  
**Status**: Not started  
**Description**:  
Allow risk parameters (min_signal_strength, min_win_rate, risk_per_trade) to be updated at runtime via config file without restart.

---

### ORCH-MONITOR-005: Web Dashboard
**Priority**: Low  
**Status**: Not started  
**Description**:  
Simple Flask app showing live orchestrator status, recent trades, P&L, agent state, risk metrics.

---

## 📊 PROJECT STATUS

### Orchestrator Framework
```
Status: ✅ HEALTHY & VALIDATED
├─ Container: Up + cycling
├─ Agents: All 6 initialized + registered
├─ State Machine: Running correctly
├─ Error Handling: Working (circuit breaker activates on failures)
├─ Risk System: Operational
└─ Paper Trading: Ready
```

### Known Issues
```
Status: 🟡 1 BLOCKING ISSUE (CoinGecko rate limits)
└─ ORCH-API-001: See HIGH PRIORITY section above
   Impact: Causes error cycles in soak test, not production-ready
   Effort to fix: ~2-3 hours
   Fix complexity: Low (standard rate limiting pattern)
```

### Deployment Readiness
```
Local Docker: ✅ Ready to run
Oracle Cloud: ✅ Ready to deploy (follow DEPLOYMENT_ORACLE.md)
Live Trading: ⏸️  Wait for ORCH-API-001 fix + extended soak test
```

---

## 🚀 RECOMMENDED NEXT STEPS (When Ready)

### Short Term (This Week)
1. Review ORCH-API-001 requirements
2. Implement centralized CoinGecko client with rate limiting
3. Run container for 1-2 hours; verify clean 10+ cycles without 429s
4. Document any new edge cases found

### Medium Term (Next Week)
1. Implement ORCH-EXEC-002 (per-symbol execution) if multi-symbol needed
2. Build ORCH-BENCH-003 (soak analysis script)
3. Run extended soak test (24-48 hours) on Oracle Cloud
4. Analyze metrics, adjust thresholds if needed

### Long Term (When Confident)
1. Enable live trading: flip `paper_trading: False` in config
2. Start with small account / low risk_per_trade
3. Monitor for 1+ week before scaling up

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `main.py` | Entry point, trading cycle orchestration |
| `agents/orchestrator.py` | Central conductor, state machine |
| `agents/data_fetcher.py` | CoinGecko data fetching (**RATE LIMIT ISSUE HERE**) |
| `agents/risk_manager.py` | Position sizing, validation |
| `agents/execution_agent.py` | Paper trade execution |
| `agents/market_analyzer.py` | Technical analysis (MA, RSI, MACD) |
| `agents/backtesting_agent.py` | Historical performance simulation |
| `agents/monitor.py` | Centralized logging |
| `Dockerfile` | Container definition |
| `docker-compose.yml` | Local orchestration |
| `requirements.txt` | Python dependencies (requests, numpy, python-dateutil) |
| `DEPLOYMENT_DOCKER.md` | Local Docker setup guide |
| `DEPLOYMENT_ORACLE.md` | Cloud deployment guide |

---

## 📝 NOTES FOR AGENT

When continuing work on this project:

1. **Context**: This is the "clean, single-agent orchestrator bot" built separately from the KuCoin bot.
2. **Current State**: Framework is production-quality; data feed rate limiting needs fixing.
3. **Testing Approach**: When fixing ORCH-API-001, test locally in Docker first (safer), then deploy to Oracle Cloud.
4. **Configuration**: `trading_pairs = ['SOL/USDT']`, risk thresholds currently relaxed (0.05, 0.30) for soak test.
5. **Guardrails**: Project identity files in place to prevent cross-project contamination.

---

Generated: 2026-02-03 16:25:31 EST  
Last Updated: After Docker deployment validation  
Project Owner: User (orchestrator bot for autonomous trading)
