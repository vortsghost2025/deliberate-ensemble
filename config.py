# Multi-Agent Trading Bot Configuration File
# Active configuration - copied from template and customized

# Core Trading Configuration
TRADING_CONFIG = {
    'account_balance': 100,             # Starting capital in USD - MICRO-LIVE TEST
    'paper_trading': True,              # True = simulate, False = LIVE TRADING (API timestamp issue - fixing)
    'trading_pairs': ['SOL/USDT'],      # Pairs to trade (SOL only for micro-live)
}

# Risk Management (CRITICAL - Do not modify lightly)
RISK_CONFIG = {
    'risk_per_trade': 0.01,             # 1% - NEVER CHANGE THIS ($1 per trade at $100 balance)
    'min_risk_reward_ratio': 1.5,       # Minimum profit:loss ratio
    'max_daily_loss': 0.05,             # 5% max daily loss ($5 at $100 balance)
    'account_balance': 100,             # Same as above - MICRO-LIVE TEST
    'min_signal_strength': 0.10,        # Minimum signal strength (lowered from 0.3 to allow weaker signals)
    'min_win_rate': 0.45,               # Minimum backtest win rate
    'min_notional_usd': 1.0,            # Minimum trade size in USD (lowered for $100 micro-live account)
    'default_stop_loss_pct': 0.02,      # 2% stop loss by default
    'enforce_min_position_size_only': True,  # MICRO TEST MODE: Use minimum position sizing only (0.01 SOL = ~$0.87)
    'min_position_size_units': 0.01,    # Default minimum (0.01 SOL)
    'min_position_size_by_pair': {
        'SOL/USDT': 0.01,               # Minimum 0.01 SOL per trade (~$0.87)
        'BTC/USDT': 0.0001,             # Minimum 0.0001 BTC per trade if enabled later
    }
}

# Market Analysis
MARKET_CONFIG = {
    'rsi_period': 14,                   # RSI calculation period
    'macd_fast': 12,                    # MACD fast period
    'macd_slow': 26,                    # MACD slow period
    'macd_signal': 9,                   # MACD signal period
    'downtrend_threshold': -5,          # % drop to trigger bearish (-5%)
}

# Backtesting
BACKTEST_CONFIG = {
    'min_win_rate': 0.45,               # Minimum acceptable win rate
    'max_drawdown': 0.15,               # Maximum acceptable drawdown (15%)
}

# Data Fetching
DATA_CONFIG = {
    'cache_timeout': 300,               # 5 minutes between API calls
    'api_timeout': 10,                  # 10 second timeout per API call
}

# KuCoin API Credentials (LIVE TRADING)
API_CONFIG = {
    'api_key': '69713960cb7e89000126f2f6',
    'api_secret': 'a6b08fdc-045e-4cf4-bafb-c60984fb7b05',
    'api_passphrase': '134679Rosebud!',
}

# Execution
EXECUTION_CONFIG = {
    'paper_trading': False,             # True = paper, False = LIVE TRADING
    'max_open_positions': 1,            # Max concurrent open trades (conservative for micro-live)
}

# Entry Timing Validation (Maximum Restraint Approach)
# Prevents premature entries during mid-candle downswings
ENTRY_TIMING_CONFIG = {
    'enabled': True,                    # Enable entry timing validation
    'reversal_threshold_pct': 0.001,    # 0.1% - Wait for price reversal confirmation
}

# Monitoring & Logging
MONITOR_CONFIG = {
    'logs_dir': './logs',               # Directory for log files
    'enable_alerts': True,              # Console alerts for events
    'alert_level': 'WARNING',           # Minimum alert level
}
