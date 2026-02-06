# Multi-Agent Trading Bot Configuration File
# Active configuration - copied from template and customized

# Core Trading Configuration
TRADING_CONFIG = {
    'account_balance': 10000,           # Starting capital in USD
    'paper_trading': True,              # True = simulate, False = LIVE TRADING
    'trading_pairs': ['SOL/USDT'],      # Pairs to trade (starting with SOL only)
}

# Risk Management (CRITICAL - Do not modify lightly)
RISK_CONFIG = {
    'risk_per_trade': 0.01,             # 1% - NEVER CHANGE THIS
    'min_risk_reward_ratio': 1.5,       # Minimum profit:loss ratio
    'max_daily_loss': 0.05,             # 5% max daily loss
    'account_balance': 10000,           # Same as above
    'min_signal_strength': 0.10,        # Minimum signal strength (lowered from 0.3 to allow weaker signals)
    'min_win_rate': 0.45,               # Minimum backtest win rate
    'min_notional_usd': 10.0,           # Minimum trade size in USD
    'default_stop_loss_pct': 0.02,      # 2% stop loss by default
    'enforce_min_position_size_only': False,  # Use dynamic position sizing based on risk
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

# Execution
EXECUTION_CONFIG = {
    'paper_trading': True,              # True = paper, False = live
    'max_open_positions': 3,            # Max concurrent open trades
}

# Monitoring & Logging
MONITOR_CONFIG = {
    'logs_dir': './logs',               # Directory for log files
    'enable_alerts': True,              # Console alerts for events
    'alert_level': 'WARNING',           # Minimum alert level
}
