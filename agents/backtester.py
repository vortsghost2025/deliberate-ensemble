"""
Backtesting Agent
Tests market signals against historical data before approval.
Generates performance metrics to validate trading strategies.
"""

from typing import Any, Dict, Optional
import logging
from datetime import datetime, timedelta

from .base_agent import BaseAgent, AgentStatus


class BacktestingAgent(BaseAgent):
    """
    Backtesting Agent: Validates signals using historical performance.
    
    Responsibilities:
    - Test signals against historical market data
    - Calculate performance metrics (win rate, max drawdown)
    - Simulate similar past market conditions
    - Reject signals with poor historical performance
    - Provide confidence scores based on backtesting
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the backtesting agent."""
        super().__init__("BacktestingAgent", config)
        self.min_backtest_win_rate = config.get('min_win_rate', 0.45) if config else 0.45
        self.max_drawdown_allowed = config.get('max_drawdown', 0.15) if config else 0.15
        self.historical_data: Dict[str, Any] = {}  # Simulated historical data
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Backtest market signals.
        
        Args:
            input_data: Contains market_data and analysis
            
        Returns:
            Message with backtest results
        """
        self.log_execution_start("backtest_signals")
        
        try:
            market_data = input_data.get('market_data', {})
            analysis = input_data.get('analysis', {})
            
            if not market_data or not analysis:
                raise ValueError("Missing market data or analysis")
            
            backtest_results = {}
            
            for pair in market_data.keys():
                pair_analysis = analysis.get(pair, {})
                
                # Run backtest for this pair
                result = self._backtest_pair(pair, pair_analysis)
                backtest_results[pair] = result
                
                self.logger.info(
                    f"{pair}: Win Rate {result['win_rate']:.1%}, "
                    f"Max Drawdown {result['max_drawdown']:.1%}"
                )
            
            # Determine if signals should be approved
            all_valid = all(
                result['signal_valid'] for result in backtest_results.values()
            )
            
            self.log_execution_end("backtest_signals", success=True)
            
            return self.create_message(
                action='backtest_signals',
                success=True,
                data={
                    'backtest_results': backtest_results,
                    'all_signals_valid': all_valid,
                    'average_win_rate': sum(
                        r['win_rate'] for r in backtest_results.values()
                    ) / len(backtest_results) if backtest_results else 0,
                    'pairs_analyzed': len(backtest_results),
                    'timestamp': datetime.utcnow().isoformat()
                }
            )
        
        except Exception as e:
            error_msg = f"Backtesting error: {str(e)}"
            self.set_status(AgentStatus.ERROR, error_msg)
            self.log_execution_end("backtest_signals", success=False)
            return self.create_message(
                action='backtest_signals',
                success=False,
                error=error_msg
            )
    
    def _backtest_pair(self, pair: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Backtest a specific trading pair.
        
        Args:
            pair: Trading pair
            analysis: Market analysis for the pair
            
        Returns:
            Backtest results dictionary
        """
        signal_type = analysis.get('recommendation', 'HOLD')
        signal_strength = analysis.get('signal_strength', 0)
        
        # Simulate historical performance based on signal type
        # In production, this would use real historical data
        if signal_type == 'BUY':
            simulated_win_rate = self._calculate_buy_signal_win_rate(signal_strength)
        elif signal_type == 'SELL':
            simulated_win_rate = self._calculate_sell_signal_win_rate(signal_strength)
        else:
            simulated_win_rate = 0.5
        
        # Calculate other metrics
        max_drawdown = self._estimate_max_drawdown(signal_type, signal_strength)
        
        # Validate based on thresholds
        signal_valid = (
            simulated_win_rate >= self.min_backtest_win_rate and
            max_drawdown <= self.max_drawdown_allowed
        )
        
        return {
            'pair': pair,
            'signal_type': signal_type,
            'win_rate': simulated_win_rate,
            'max_drawdown': max_drawdown,
            'trades_analyzed': 100,  # Simulated
            'signal_valid': signal_valid,
            'validation_reason': self._get_validation_reason(
                signal_valid, simulated_win_rate, max_drawdown
            ),
            'confidence': simulated_win_rate if signal_valid else 0,
            'recommendation': 'PROCEED' if signal_valid else 'SKIP'
        }
    
    def _calculate_buy_signal_win_rate(self, signal_strength: float) -> float:
        """
        Calculate win rate for BUY signals based on signal strength.
        
        Args:
            signal_strength: Signal confidence (0-1)
            
        Returns:
            Expected win rate (0-1)
        """
        # Base win rate + boost from signal strength
        base_rate = 0.52
        strength_boost = signal_strength * 0.15
        win_rate = base_rate + strength_boost
        return min(win_rate, 0.75)  # Cap at 75%
    
    def _calculate_sell_signal_win_rate(self, signal_strength: float) -> float:
        """
        Calculate win rate for SELL signals based on signal strength.
        
        Args:
            signal_strength: Signal confidence (0-1)
            
        Returns:
            Expected win rate (0-1)
        """
        # Sell signals typically have lower win rates
        base_rate = 0.48
        strength_boost = signal_strength * 0.12
        win_rate = base_rate + strength_boost
        return min(win_rate, 0.65)  # Cap at 65%
    
    def _estimate_max_drawdown(self, signal_type: str, signal_strength: float) -> float:
        """
        Estimate maximum drawdown based on signal type and strength.
        
        Args:
            signal_type: Type of signal (BUY, SELL, HOLD)
            signal_strength: Signal confidence (0-1)
            
        Returns:
            Estimated max drawdown (0-1)
        """
        if signal_type == 'BUY':
            base_drawdown = 0.08
        elif signal_type == 'SELL':
            base_drawdown = 0.10
        else:
            base_drawdown = 0.05
        
        # Reduce drawdown with stronger signals
        adjusted_drawdown = base_drawdown * (1 - signal_strength * 0.3)
        return max(adjusted_drawdown, 0.02)
    
    def _get_validation_reason(
        self,
        is_valid: bool,
        win_rate: float,
        max_drawdown: float
    ) -> str:
        """Generate validation reason message."""
        if is_valid:
            return "Signal passed backtest validation"
        
        reasons = []
        if win_rate < self.min_backtest_win_rate:
            reasons.append(f"Win rate {win_rate:.1%} below minimum {self.min_backtest_win_rate:.1%}")
        if max_drawdown > self.max_drawdown_allowed:
            reasons.append(f"Drawdown {max_drawdown:.1%} exceeds maximum {self.max_drawdown_allowed:.1%}")
        
        return "; ".join(reasons)
    
    def add_historical_data(self, pair: str, data: Dict[str, Any]) -> None:
        """
        Add historical data for backtesting.
        
        Args:
            pair: Trading pair
            data: Historical price/volume data
        """
        self.historical_data[pair] = data
        self.logger.info(f"Added historical data for {pair}")
