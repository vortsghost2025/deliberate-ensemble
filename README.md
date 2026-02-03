# Multi-Agent Autonomous Trading Bot 🤖

A sophisticated Python-based cryptocurrency trading system using a multi-agent architecture with autonomous orchestration. Each agent has a single responsibility and coordinates through a central orchestrator.

## System Architecture

### 🧠 Agent Orchestra

The system implements the **Actor Model** pattern where independent agents communicate through a central orchestrator:

```
┌─────────────────────────────────────────────┐
│     ORCHESTRATOR AGENT (Main Conductor)     │
│  • Workflow management                      │
│  • Safety circuit breaker                   │
│  • Downtrend protection                     │
└────────────┬────────────────────────────────┘
             │
    ┌────────┴─────────┬──────────┬──────────┬──────────┐
    │                  │          │          │          │
    ▼                  ▼          ▼          ▼          ▼
┌─────────┐    ┌────────────┐ ┌──────┐ ┌─────────┐ ┌────────┐
│ Data    │    │ Market     │ │Risk  │ │Backtest │ │Executor│
│Fetcher  │    │Analyzer    │ │Mgmt  │ │         │ │        │
├─────────┤    ├────────────┤ ├──────┤ ├─────────┤ ├────────┤
│ Async   │    │ RSI/MACD   │ │1% Max│ │Historical│Simulate│
│Caching  │    │ Downtrend  │ │Risk  │ │Win Rate  │Trades  │
└─────────┘    │ Detection  │ │Check │ │Validation│ (Paper)│
               └────────────┘ └──────┘ └─────────┘ └────────┘
                    │          │           │          │
                    └──────────┴───────────┴──────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Monitor Agent    │
                    │ • Logging        │
                    │ • Alerts         │
                    │ • Performance    │
                    └──────────────────┘
```

## Agent Responsibilities

### 1. **Orchestrator Agent** - The Brain
- **Role**: Orchestrates the entire workflow
- **Responsibilities**:
  - Manage workflow state transitions
  - Enforce safety circuit breaker
  - Block trades during downtrends (KEY SAFETY FEATURE)
  - Coordinate handoffs between agents
  - Handle errors and recovery
  - Maintain workflow history

### 2. **Data Fetching Agent** - Market Eyes
- **Role**: Real-time market data acquisition
- **Features**:
  - Async API calls (CoinGecko, DeFiLlama)
  - 5-minute caching to reduce API calls
  - Automatic data normalization
  - Multi-pair support
- **Free APIs Used**:
  - CoinGecko (price, volume, 24h changes)
  - DeFiLlama (on-chain metrics)

### 3. **Market Analysis Agent** - Market Reader
- **Role**: Technical analysis and trend detection
- **Capabilities**:
  - RSI calculation and interpretation
  - MACD signal generation
  - Trend classification (uptrend, downtrend, sideways)
  - **CRITICAL**: Downtrend detection blocks all trades
  - Market regime classification
  - Signal generation with confidence scores

### 4. **Risk Management Agent** - Safety Guard ⚠️
- **Role**: Enforces strict risk controls
- **Core Rules**:
  - **Never risk more than 1% of capital per trade** (strict enforced)
  - Calculate position sizes dynamically
  - Generate stop-loss levels (2% below entry)
  - Calculate take-profit with minimum 1.5:1 risk-reward ratio
  - Reject any trade violating thresholds
  - Track cumulative daily risk

### 5. **Backtesting Agent** - Quality Control
- **Role**: Signal validation through history
- **Functions**:
  - Test signals against simulated historical data
  - Calculate win rate expectations
  - Estimate max drawdown
  - Reject signals with poor historical performance
  - Provide confidence scores

### 6. **Execution Agent** - Trade Handler
- **Role**: Execute trades with full tracking
- **Features**:
  - **Paper trading by default** (no real money)
  - Track open positions
  - Monitor profit/loss in real-time
  - Calculate performance metrics
  - Ready for live exchange integration
- **Paper Trading Metrics**:
  - Win rate
  - Total P&L
  - Max drawdown
  - Trade history

### 7. **Monitoring Agent** - System Logger
- **Role**: Centralized logging and alerting
- **Functions**:
  - Log all agent decisions
  - Generate performance reports
  - Create console alerts for important events
  - Maintain audit trail (JSON event logs)
  - Track system health

## Safety Features 🛡️

### 1. **Downtrend Protection** (CRITICAL)
- Market Analysis Agent detects bearish conditions
- Orchestrator automatically pauses all trading
- Message: "Bearish market regime detected - downtrend protection active"

### 2. **Risk Per Trade Cap**
- Never exceeds 1% of account balance
- Risk Management Agent enforces this strictly
- Account balance: $10,000 default → max $100 risk per trade

### 3. **Daily Loss Limit**
- Maximum 5% daily loss allowed
- Once reached, no more trades for the day
- Can be reset next trading day

### 4. **Circuit Breaker**
- Automatic emergency stop on critical failures
- Blocks all trading immediately
- Requires manual intervention to reset

### 5. **Risk-Reward Ratio Enforcement**
- Minimum 1.5:1 ratio on all trades
- Profit target ≥ 1.5 × stop loss distance
- Protects against unfavorable setups

## Workflow: Trade Decision Pipeline

```
1. DATA FETCHING
   └─> Fetch prices, volume, 24h changes for all pairs
   
2. MARKET ANALYSIS
   └─> Calculate technical indicators
   └─> [SAFETY CHECK] Detect downtrend → PAUSE if bearish
   
3. BACKTESTING
   └─> Validate signals against historical performance
   
4. RISK MANAGEMENT
   └─> Calculate position size (max 1% risk)
   └─> Generate stop-loss and take-profit
   └─> [SAFETY CHECK] Reject if risk thresholds breached
   
5. EXECUTION
   └─> Execute trade (paper trading by default)
   └─> Track position
   
6. MONITORING
   └─> Log all decisions
   └─> Generate alerts
   └─> Update performance metrics
```

## Quick Start

### Installation

```bash
# Clone or navigate to project directory
cd trading-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Bot

```bash
# Run single trading cycle (paper trading)
python main.py

# The bot will:
# 1. Initialize all 6 agents
# 2. Fetch current market data
# 3. Analyze market conditions
# 4. Check for downtrends (safety feature)
# 5. Backtest signals
# 6. Calculate position sizing
# 7. Execute paper trades
# 8. Log all activity
```

### Configuration

Edit `main.py` to customize settings:

```python
config = {
    'risk_manager': {
        'account_balance': 10000,      # Your trading capital
        'risk_per_trade': 0.01,        # 1% (don't change - core rule)
        'min_risk_reward_ratio': 1.5,  # Minimum RR ratio
        'max_daily_loss': 0.05         # 5% daily limit
    },
    'market_analyzer': {
        'downtrend_threshold': -5      # Flag bearish if -5% or worse
    },
    'executor': {
        'paper_trading': True          # Set to False for live trading (DANGEROUS!)
    }
}
```

## Trading Pairs

Default trading pairs (modify in `main.py`):
- `SOL/USDT` - Solana (primary focus)
- `BTC/USDT` - Bitcoin
- `ETH/USDT` - Ethereum

Supported pairs (expandable):
- SOL, BTC, ETH, RAY, ORCA, COPE, USDC, USDT, and more

## Output Files

After running, check these files:

```
logs/
├── trading_bot.log        # Full system logs
├── events.jsonl           # Structured event log (JSON Lines)
└── (performance graphs - future)
```

Example log entry:
```json
{
  "timestamp": "2025-02-02T14:30:45.123456",
  "workflow_stage": "monitoring",
  "data_fetch": {"success": true, "symbols_count": 2},
  "market_analysis": {"regime": "sideways", "downtrend_detected": false},
  "risk_assessment": {"position_approved": true, "position_size": 0.05},
  "execution": {"trade_executed": true, "trade_id": 1}
}
```

## Extending the System

### Adding a New Agent

1. Create new file: `agents/my_agent.py`
2. Inherit from `BaseAgent`:
```python
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__("MyAgent", config)
    
    def execute(self, input_data):
        # Your logic here
        return self.create_message(
            action='my_action',
            success=True,
            data={...}
        )
```

3. Register in `main.py`:
```python
my_agent = MyAgent(config.get('my_agent', {}))
orchestrator.register_agent(my_agent)
```

### Adding Support for Live Trading

1. Modify `ExecutionAgent.execute()` to detect `paper_trading=False`
2. Integrate exchange API (CCXT already installed):
```python
import ccxt

exchange = ccxt.binance({'apiKey': '...', 'secret': '...'})
order = exchange.create_limit_buy_order('SOL/USDT', amount, price)
```

### Adding Exchange Support

The bot already includes CCXT library. To add exchange support:

```python
# In data_fetcher.py or new agent
import ccxt

exchange = ccxt.binance()  # or: ccxt.kucoin(), ccxt.ftx(), etc.
ticker = exchange.fetch_ticker('SOL/USDT')
```

## Performance Tracking

The Execution Agent automatically tracks:
- **Win Rate**: % of profitable trades
- **Total P&L**: Profit/loss across all trades
- **Max Drawdown**: Largest loss from peak
- **Max Win/Loss**: Best and worst trade
- **Open Positions**: Currently active trades

View stats after each cycle:
```
Final Performance Summary:
  Total Trades: 5
  Winning: 3 | Losing: 2
  Win Rate: 60.0%
  Total P&L: $127.50
  Average P&L: $25.50
  Max Win: $75.00 | Max Loss: -$22.50
  Open Positions: 1
```

## Safety Reminders ⚠️

1. **PAPER TRADING BY DEFAULT**: No real money is used unless explicitly changed
2. **DOWNTREND PROTECTION**: Automatically stops trading in bear markets
3. **1% RISK RULE**: Never risked more than 1% per trade (enforced)
4. **TEST THOROUGHLY**: Run in paper trading mode for weeks before going live
5. **MONITOR ACTIVELY**: Check logs regularly for unexpected behavior
6. **BACKUP DATA**: Save event logs regularly

## Troubleshooting

### No data fetched
- Check internet connection
- CoinGecko API might be rate-limited (waits 60s)
- Verify trading pairs are correct

### Trades not executing
- Market Analysis detected bearish conditions (check logs)
- Risk Manager rejected (position size too large for win rate)
- Backtesting failed (historical performance too poor)

### Memory issues
- Increase cache timeout in config
- Reduce trading pair count
- Monitor `logs/trading_bot.log`

## Future Enhancements

- [ ] Live trading integration (Binance, Kucoin, Solana DEXs)
- [ ] Advanced technical indicators (Bollinger Bands, Stochastic)
- [ ] Machine learning signal generation
- [ ] Portfolio rebalancing agent
- [ ] Sentiment analysis integration
- [ ] Advanced visualization dashboard
- [ ] Multi-timeframe analysis
- [ ] Options trading support

## Architecture Benefits

✅ **Modularity**: Each agent is independent and testable  
✅ **Scalability**: Easy to add new agents  
✅ **Safety**: Multiple validation layers before execution  
✅ **Maintainability**: Clear separation of concerns  
✅ **Testability**: Each agent can be tested in isolation  
✅ **Observability**: Comprehensive logging and alerts  
✅ **Flexibility**: Swap agents without affecting others  

## License

This project is provided as-is for educational purposes.

---

**Built with ❤️ for autonomous, safe, and intelligent trading**
