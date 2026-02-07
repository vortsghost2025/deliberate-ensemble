"""
Verify the position sizing fix - simulate risk manager calculation
"""

# Config values from config.py
account_balance = 100
risk_per_trade = 0.01  # 1%
min_signal_strength = 0.10
default_stop_loss_pct = 0.02  # 2%
min_notional_usd = 1.0  # FIXED from 10.0

# Market data
sol_price = 87.00
signal_strength = 0.10  # Weak signal (minimum threshold)
win_rate = 0.50

# Calculate position sizing (from risk_manager.py logic)
print("=" * 60)
print("POSITION SIZING VERIFICATION")
print("=" * 60)

# Step 1: Max risk amount
max_risk_amount = account_balance * risk_per_trade
print(f"\n1. Max risk amount: ${max_risk_amount:.2f} (1% of ${account_balance})")

# Step 2: Adjust for confidence
confidence_multiplier = signal_strength * win_rate
actual_risk_amount = max_risk_amount * confidence_multiplier
print(f"2. Confidence multiplier: {signal_strength:.2f} × {win_rate:.2f} = {confidence_multiplier:.2f}")
print(f"   Actual risk: ${actual_risk_amount:.2f}")

# Step 3: Stop loss
stop_loss = sol_price * (1 - default_stop_loss_pct)
print(f"3. Stop loss: ${stop_loss:.2f} (2% below ${sol_price:.2f})")

# Step 4: Risk per unit
risk_per_unit = sol_price - stop_loss
print(f"4. Risk per unit: ${risk_per_unit:.2f}")

# Step 5: Position size
position_size = actual_risk_amount / risk_per_unit
print(f"5. Position size: {position_size:.4f} SOL")

# Step 6: Notional value
position_size_usd = position_size * sol_price
print(f"6. Notional value: ${position_size_usd:.2f}")

# Step 7: Check minimum notional
print(f"\n7. Minimum notional check:")
print(f"   Notional: ${position_size_usd:.2f}")
print(f"   Minimum: ${min_notional_usd:.2f}")

if position_size_usd < min_notional_usd:
    print(f"   ❌ REJECTED - Below minimum")
else:
    print(f"   ✅ APPROVED - Above minimum")

print("\n" + "=" * 60)
print("COMPARISON: OLD vs NEW CONFIG")
print("=" * 60)
print(f"\nOLD: min_notional_usd = $10.00")
print(f"  → Position notional ${position_size_usd:.2f} < $10.00 = REJECTED ❌")
print(f"\nNEW: min_notional_usd = $1.00")
print(f"  → Position notional ${position_size_usd:.2f} > $1.00 = APPROVED ✅")
print("\n" + "=" * 60)
