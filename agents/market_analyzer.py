"""
Market Analysis Agent
Performs technical analysis and market regime classification.
Implements critical downtrend detection safety feature.
Includes entry timing validation to prevent mid-downswing purchases.
"""

import numpy as np
from typing import Any, Dict, Optional, List
from enum import Enum
import logging
import sys
import os

# Add parent directory to path for entry_timing_validator import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent, AgentStatus

try:
    from entry_timing_validator import EntryTimingValidator
    ENTRY_TIMING_AVAILABLE = True
except ImportError:
    ENTRY_TIMING_AVAILABLE = False
    EntryTimingValidator = None


class MarketRegime(Enum):
    """Classification of current market regime."""
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"
    HIGH_VOLATILITY = "high_volatility"
    UNKNOWN = "unknown"


class MarketAnalysisAgent(BaseAgent):
    """
    Market Analysis Agent: Analyzes market conditions and detects trends.
    
    Responsibilities:
    - Calculate technical indicators (RSI, MACD, moving averages)
    - Classify market regime
    - Detect downtrends (CRITICAL SAFETY FEATURE)
    - Calculate volatility
    - Identify support/resistance levels
    - Generate trading signals with confidence scores
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the market analysis agent."""
        super().__init__("MarketAnalysisAgent", config)
        self.rsi_period = config.get('rsi_period', 14) if config else 14
        self.macd_fast = config.get('macd_fast', 12) if config else 12
        self.macd_slow = config.get('macd_slow', 26) if config else 26
        self.macd_signal = config.get('macd_signal', 9) if config else 9
        self.downtrend_threshold = config.get('downtrend_threshold', -5) if config else -5
        
        # Initialize entry timing validator (maximum restraint approach)
        self.entry_timing_enabled = False
        self.entry_timing_validator = None
        
        if ENTRY_TIMING_AVAILABLE and config:
            entry_config = config.get('entry_timing_config', {})
            if entry_config.get('enabled', False):
                threshold_pct = entry_config.get('reversal_threshold_pct', 0.001)
                self.entry_timing_validator = EntryTimingValidator(threshold_pct)
                self.entry_timing_enabled = True
                self.logger.info(f"[ENTRY TIMING] Enabled with {threshold_pct*100:.1f}% reversal threshold")
            else:
                self.logger.info("[ENTRY TIMING] Disabled in config")
        elif not ENTRY_TIMING_AVAILABLE:
            self.logger.warning("[ENTRY TIMING] Module not available (import failed)")
        else:
            self.logger.info("[ENTRY TIMING] Not configured")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market data and generate signals.
        
        Args:
            input_data: Must contain 'market_data' dictionary
            
        Returns:
            Message with analysis results
        """
        self.log_execution_start("analyze_market")
        
        try:
            # Handle both direct market_data dict or nested in 'data'
            market_data = input_data.get('market_data', {})
            if isinstance(market_data, dict) and 'data' in market_data:
                market_data = market_data.get('data', {})
            
            if not market_data or isinstance(market_data, int):
                raise ValueError("No valid market data provided")
            
            analysis_results = {}
            has_bearish = False
            
            for pair, data in market_data.items():
                if not isinstance(data, dict):
                    continue
                    
                self.logger.info(f"Analyzing {pair}")
                
                # Analyze this pair
                pair_analysis = self._analyze_pair(pair, data)
                analysis_results[pair] = pair_analysis
                
                # Check for bearish regime
                if pair_analysis['regime'] == MarketRegime.BEARISH.value:
                    has_bearish = True
                    self.logger.warning(f"[WARN] BEARISH REGIME DETECTED for {pair}")
            
            # Determine overall market regime
            overall_regime = self._determine_overall_regime(analysis_results)
            
            # Safety feature: Flag if any downtrend detected
            downtrend_detected = has_bearish or overall_regime == MarketRegime.BEARISH.value
            
            self.log_execution_end("analyze_market", success=True)
            
            return self.create_message(
                action='analyze_market',
                success=True,
                data={
                    'analysis': analysis_results,
                    'regime': overall_regime,
                    'downtrend_detected': downtrend_detected,
                    'pairs_analyzed': len(analysis_results),
                    'signal_confidence': self._calculate_overall_confidence(analysis_results)
                }
            )
        
        except Exception as e:
            error_msg = f"Market analysis error: {str(e)}"
            self.set_status(AgentStatus.ERROR, error_msg)
            self.log_execution_end("analyze_market", success=False)
            return self.create_message(
                action='analyze_market',
                success=False,
                error=error_msg
            )
    
    def _analyze_pair(self, pair: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single trading pair.
        
        Args:
            pair: Trading pair identifier
            data: Market data for the pair
            
        Returns:
            Analysis dictionary for the pair
        """
        current_price = data.get('current_price', 0)
        price_change_24h = data.get('price_change_24h_pct', 0)
        volume_24h = data.get('volume_24h', 0)
        
        # Calculate simple indicators based on 24h change
        # In production, you'd use historical price data for better indicators
        
        # RSI simulation (based on price change momentum)
        rsi = self._calculate_rsi_simple(price_change_24h)
        
        # MACD signal (simplified)
        macd_signal = self._calculate_macd_simple(price_change_24h)
        
        # Trend determination
        trend = self._determine_trend(price_change_24h, rsi)
        
        # Volatility classification
        volatility = self._classify_volatility(price_change_24h)
        
        # Market regime
        regime = self._classify_regime(price_change_24h, rsi, volatility)
        
        # Buy/Sell signal (0-100, 50 is neutral)
        signal = self._generate_signal(price_change_24h, rsi)
        
        # Entry timing validation (maximum restraint)
        entry_timing_approved = True
        entry_timing_reason = "Not configured"
        
        if self.entry_timing_enabled and self.entry_timing_validator:
            entry_timing_approved, entry_timing_reason = \
                self.entry_timing_validator.check_reversal_confirmation(pair, current_price)
            
            if not entry_timing_approved:
                self.logger.info(f"[{pair}] Entry timing DEFERRED: {entry_timing_reason}")
        
        return {
            'pair': pair,
            'current_price': current_price,
            'price_change_24h': price_change_24h,
            'rsi': rsi,
            'macd_signal': macd_signal,
            'trend': trend,
            'volatility': volatility,
            'regime': regime,
            'buy_signal': signal,
            'signal_strength': abs(signal - 50) / 50,  # 0-1, higher = stronger
            'recommendation': 'BUY' if signal > 60 else 'SELL' if signal < 40 else 'HOLD',
            'entry_timing_approved': entry_timing_approved,
            'entry_timing_reason': entry_timing_reason
        }
    
    def _calculate_rsi_simple(self, price_change: float) -> float:
        """
        Simplified RSI calculation based on recent price change.
        In production, use full RSI with more history.
        
        Args:
            price_change: 24h price change percentage
            
        Returns:
            RSI value (0-100)
        """
        # Map price change to RSI
        # Positive change = higher RSI, negative = lower RSI
        rsi = 50 + (price_change / 10)  # Scale the change
        return max(0, min(100, rsi))
    
    def _calculate_macd_simple(self, price_change: float) -> float:
        """Simplified MACD signal."""
        return price_change * 2
    
    def _determine_trend(self, price_change: float, rsi: float) -> str:
        """Determine trend direction."""
        if price_change > 2 or rsi > 60:
            return 'uptrend'
        elif price_change < -2 or rsi < 40:
            return 'downtrend'
        else:
            return 'sideways'
    
    def _classify_volatility(self, price_change: float) -> str:
        """Classify volatility level."""
        abs_change = abs(price_change)
        if abs_change > 10:
            return 'high'
        elif abs_change > 5:
            return 'medium'
        else:
            return 'low'
    
    def _classify_regime(self, price_change: float, rsi: float, volatility: str) -> str:
        """
        Classify overall market regime.
        CRITICAL: Return 'bearish' for downtrend protection.
        """
        # If price changed significantly downward, it's bearish
        if price_change < self.downtrend_threshold:
            return MarketRegime.BEARISH.value
        
        # If RSI is in oversold territory, it's bearish
        if rsi < 30:
            return MarketRegime.BEARISH.value
        
        # High volatility regime
        if volatility == 'high':
            return MarketRegime.HIGH_VOLATILITY.value
        
        # Bullish indicators
        if price_change > 2 and rsi > 50:
            return MarketRegime.BULLISH.value
        
        # Default to sideways
        return MarketRegime.SIDEWAYS.value
    
    def _generate_signal(self, price_change: float, rsi: float) -> float:
        """
        Generate buy/sell signal.
        
        Returns:
            Signal value 0-100 (50=neutral, >60=buy, <40=sell)
        """
        signal = 50
        
        # Price change component
        signal += price_change * 2
        
        # RSI component
        signal += (rsi - 50) * 0.5
        
        return max(0, min(100, signal))
    
    def _determine_overall_regime(self, analysis: Dict[str, Dict]) -> str:
        """Determine overall market regime from all pairs."""
        regimes = [pair_analysis.get('regime') for pair_analysis in analysis.values()]
        
        # If any pair is bearish, entire market is bearish
        if MarketRegime.BEARISH.value in regimes:
            return MarketRegime.BEARISH.value
        
        # Count regimes
        bullish_count = sum(1 for r in regimes if r == MarketRegime.BULLISH.value)
        high_vol_count = sum(1 for r in regimes if r == MarketRegime.HIGH_VOLATILITY.value)
        
        if len(regimes) == 0:
            return MarketRegime.UNKNOWN.value
        
        # Majority rules
        if bullish_count > len(regimes) / 2:
            return MarketRegime.BULLISH.value
        elif high_vol_count > len(regimes) / 2:
            return MarketRegime.HIGH_VOLATILITY.value
        else:
            return MarketRegime.SIDEWAYS.value
    
    def _calculate_overall_confidence(self, analysis: Dict[str, Dict]) -> float:
        """Calculate overall signal confidence."""
        if not analysis:
            return 0.0
        
        confidences = [
            pair['signal_strength'] for pair in analysis.values()
        ]
        return sum(confidences) / len(confidences) if confidences else 0.0
