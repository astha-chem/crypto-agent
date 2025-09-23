def calculate_dynamic_rsi_thresholds(asset, timeframe, lookback_period=90):
    historical_rsi = get_rsi_data(asset, timeframe, lookback_period)
    
    # Percentile-based thresholds
    oversold = np.percentile(historical_rsi, 20)  # Bottom 20%
    overbought = np.percentile(historical_rsi, 80)  # Top 20%
    
    # Market regime adjustments
    market_regime = detect_market_regime()
    if market_regime == "bull_market":
        oversold += 5  # Raise oversold threshold in bull markets
    elif market_regime == "bear_market":
        overbought -= 5  # Lower overbought threshold in bear markets
    return oversold, overbought