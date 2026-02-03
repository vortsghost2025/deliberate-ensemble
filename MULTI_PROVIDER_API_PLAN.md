# Multi-Provider CoinGecko Alternative Strategy
# ==============================================

## Problem with Current Setup
- CoinGecko free tier: ~10 req/min
- This is the bottleneck preventing continuous trading

## Solution: Multi-Provider Failover

### Provider Comparison
| Provider | Rate Limit | Auth Required | Benefit |
|----------|-----------|---------------|---------|
| Binance Public | 1200 req/min | ❌ No | PRIMARY - unlimited free |
| Kraken Public | 900 req/min | ❌ No | BACKUP - no auth needed |
| CoinGecko | 10-50 req/min | ❌ No | FALLBACK - current |

### Implementation Plan

1. **Create** `utils/multi_provider_client.py`
   - Try Binance API first (1200 req/min, no auth)
   - Fall back to Kraken if Binance fails (900 req/min, no auth)
   - Fall back to CoinGecko if both fail (10 req/min)
   - Same rate limiting envelope as current (6s minimum interval)

2. **Update** `agents/data_fetcher.py`
   - Use multi-provider client instead of single CoinGecko
   - Log which provider is being used
   - Track failover events

3. **Benefits**
   - ✅ Zero API cost (all free tiers)
   - ✅ 1000x better rate limits than CoinGecko alone
   - ✅ Built-in redundancy (if one provider is down, others take over)
   - ✅ No authentication required (public data only)

### Provider API Examples

**Binance:**
```bash
curl "https://api.binance.com/api/v3/ticker/price?symbols=%5B%22ETHUSDT%22%5D"
# Returns: {"symbol":"ETHUSDT","price":"2500.00"}
```

**Kraken:**
```bash
curl "https://api.kraken.com/0/public/Ticker?pair=ETHUSD"
# Returns ticker data in Kraken format
```

### Next Steps (After Paper Trading Soak Completes)

1. Implement `utils/multi_provider_client.py` with Binance as primary
2. Update data_fetcher to use multi-provider client
3. Run paper trading soak with new provider
4. Verify sustained cycles without 429s
5. Then deploy live with $100 or upgraded funding

### Current Status
- ✅ Paper trading soak running now (Phase 1)
- ⏳ Multi-provider implementation (Phase 2)
- ⏳ Extended soak with new providers (Phase 3)
- ⏳ Live trading ready (Phase 4)

### Cost Analysis
- **Current**: $0 (free tier) + limited to 10 req/min = bottleneck
- **New**: $0 (free tiers) + access to 1200+ req/min = unlimited within typical soak needs
- **Upgrade if needed**: CoinGecko Pro ($50/mo) gives 500 req/min, but not necessary with multi-provider

---

**Verdict:** Use multi-provider free tiers. No cost, best of all worlds.
