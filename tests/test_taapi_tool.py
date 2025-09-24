"""
Tests for TAAPI.IO API client
"""
import os
from dotenv import load_dotenv
from src.tools.taapi_tool import TaapiClient


def test_rsi_fetching():
    """
    Test function to verify RSI data retrieval for BTC/USDT and ETH/USDT
    """
    try:
        client = TaapiClient()

        # Test BTC/USDT RSI
        print("Testing BTC/USDT RSI...")
        btc_rsi = client.get_rsi('BTC/USDT')
        print(f"BTC RSI: {btc_rsi}")

        # Test ETH/USDT RSI
        print("\nTesting ETH/USDT RSI...")
        eth_rsi = client.get_rsi('ETH/USDT')
        print(f"ETH RSI: {eth_rsi}")

        # Validate response structure
        for asset, rsi_data in [('BTC', btc_rsi), ('ETH', eth_rsi)]:
            if 'value' not in rsi_data:
                print(f"WARNING: {asset} RSI response missing 'value' field")
            else:
                rsi_value = rsi_data['value']
                if not (0 <= rsi_value <= 100):
                    print(f"WARNING: {asset} RSI value {rsi_value} outside expected range [0-100]")
                else:
                    print(f"✓ {asset} RSI value {rsi_value} is valid")

        return True

    except Exception as e:
        print(f"Test failed: {e}")
        return False


def test_macd_individual():
    """
    Test MACD endpoint individually
    """
    try:
        client = TaapiClient()

        print("Testing MACD for BTC/USDT...")
        macd_data = client.get_macd('BTC/USDT')
        print(f"MACD response: {macd_data}")

        # Check for expected MACD fields
        expected_fields = ['valueMACD', 'valueMACDSignal', 'valueMACDHist']
        for field in expected_fields:
            if field in macd_data:
                print(f"✓ {field}: {macd_data[field]}")
            else:
                print(f"✗ Missing {field}")

        return True

    except Exception as e:
        print(f"MACD test failed: {e}")
        return False


def test_bollinger_individual():
    """
    Test Bollinger Bands endpoint individually
    """
    try:
        client = TaapiClient()

        print("Testing Bollinger Bands for BTC/USDT...")
        bb_data = client.get_bollinger_bands('BTC/USDT')
        print(f"Bollinger Bands response: {bb_data}")

        # Check for expected Bollinger Band fields
        expected_fields = ['valueUpperBand', 'valueMiddleBand', 'valueLowerBand']
        for field in expected_fields:
            if field in bb_data:
                print(f"✓ {field}: {bb_data[field]}")
            else:
                print(f"✗ Missing {field}")

        return True

    except Exception as e:
        print(f"Bollinger Bands test failed: {e}")
        return False


def test_bulk_indicators():
    """
    Test function to verify bulk indicator fetching for BTC/USDT
    """
    try:
        client = TaapiClient()

        print("Testing bulk indicator fetch for BTC/USDT...")
        bulk_data = client.get_multiple_indicators('BTC/USDT')

        print(f"Bulk response keys: {list(bulk_data.keys())}")

        # Validate expected indicators are present
        expected_indicators = ['rsi', 'ema_14', 'sma_50', 'macd', 'bollinger']
        missing_indicators = []

        for indicator in expected_indicators:
            if indicator not in bulk_data:
                missing_indicators.append(indicator)
            else:
                print(f"✓ {indicator}: {bulk_data[indicator]}")

        if missing_indicators:
            print(f"WARNING: Missing indicators: {missing_indicators}")
            return False

        # Validate RSI is in range
        if 'rsi' in bulk_data and 'value' in bulk_data['rsi']:
            rsi_val = bulk_data['rsi']['value']
            if not (0 <= rsi_val <= 100):
                print(f"WARNING: RSI value {rsi_val} outside range [0-100]")
                return False

        # Validate MACD has expected fields
        if 'macd' in bulk_data:
            macd_data = bulk_data['macd']
            expected_macd_fields = ['valueMACD', 'valueMACDSignal', 'valueMACDHist']
            for field in expected_macd_fields:
                if field not in macd_data:
                    print(f"WARNING: MACD missing field: {field}")

        # Validate Bollinger Bands has expected fields
        if 'bollinger' in bulk_data:
            bb_data = bulk_data['bollinger']
            expected_bb_fields = ['valueUpperBand', 'valueMiddleBand', 'valueLowerBand']
            for field in expected_bb_fields:
                if field not in bb_data:
                    print(f"WARNING: Bollinger Bands missing field: {field}")

        print("✓ All core indicators fetched successfully")
        return True

    except Exception as e:
        print(f"Bulk test failed: {e}")
        return False


def run_all_tests():
    """
    Run all TAAPI tool tests
    """
    load_dotenv()
    print("TAAPI Tool Tests")
    print("=" * 40)

    # Check if API key is available
    api_key = os.getenv('TAAPI_API_KEY')
    if not api_key:
        print("ERROR: TAAPI_API_KEY environment variable not set")
        print("Please set your TAAPI API key: export TAAPI_API_KEY='your_key_here'")
        return False

    # Run RSI test
    success = test_rsi_fetching()
    if success:
        print("\n✓ RSI data fetching successful!")
    else:
        print("\n✗ RSI data fetching failed.")

    # Test MACD individually
    print("\n" + "=" * 40)
    print("Testing MACD Individual")
    print("=" * 40)
    test_macd_individual()

    # Test Bollinger Bands individually
    print("\n" + "=" * 40)
    print("Testing Bollinger Bands Individual")
    print("=" * 40)
    test_bollinger_individual()

    # Test bulk functionality
    print("\n" + "=" * 40)
    print("Testing Bulk Query Functionality")
    print("=" * 40)

    success_bulk = test_bulk_indicators()
    if success_bulk:
        print("\n✓ Bulk indicator fetching successful!")
        return True
    else:
        print("\n✗ Bulk indicator fetching failed.")
        return False


def test_market_data():
    """
    Test market data endpoints: price, volume, candle, candles
    """
    try:
        client = TaapiClient()
        symbol = 'BTC/USDT'

        print("\n" + "=" * 40)
        print("TESTING MARKET DATA ENDPOINTS")
        print("=" * 40)

        # Test current price
        print(f"\n1. Testing current price for {symbol}...")
        price_data = client.get_price(symbol)
        print(f"Price response: {price_data}")

        current_price = price_data.get('value')
        if current_price:
            print(f"✓ Current price: ${current_price:,.2f}")
        else:
            print("✗ No price value in response")

        # Test volume
        print(f"\n2. Testing volume for {symbol}...")
        volume_data = client.get_volume(symbol)
        print(f"Volume response: {volume_data}")

        volume = volume_data.get('value')
        if volume is not None:
            print(f"✓ Volume: {volume:,.2f} ({'Green' if volume > 0 else 'Red'} candle)")
        else:
            print("✗ No volume value in response")

        # Test single candle (current)
        print(f"\n3. Testing current candle for {symbol}...")
        candle_data = client.get_candle(symbol)
        print(f"Candle response: {candle_data}")

        if 'open' in candle_data and 'close' in candle_data:
            print(f"✓ OHLC - Open: {candle_data.get('open')}, High: {candle_data.get('high')}, Low: {candle_data.get('low')}, Close: {candle_data.get('close')}")
        else:
            print("✗ Missing OHLC data in candle response")

        # Test multiple candles
        print(f"\n4. Testing last 5 candles for {symbol}...")
        candles_data = client.get_candles(symbol, period=5)

        # Handle both list and dict response formats
        if isinstance(candles_data, list):
            candles = candles_data
            print(f"Candles response: Direct list with {len(candles)} items")
            print(f"✓ Retrieved {len(candles)} candles")
        elif isinstance(candles_data, dict):
            print(f"Candles response keys: {list(candles_data.keys())}")
            if 'data' in candles_data and isinstance(candles_data['data'], list):
                candles = candles_data['data']
                print(f"✓ Retrieved {len(candles)} candles")
            else:
                print("✗ No candles data array in response")
                candles = []
        else:
            print("✗ Unexpected candles response format")
            candles = []

        # Show sample candle data if available
        if len(candles) > 0:
            first_candle = candles[0]
            print(f"✓ First candle sample: {first_candle}")

        return True

    except Exception as e:
        print(f"Market data test failed: {e}")
        return False


def test_bulk_with_market_data():
    """
    Test bulk API call with market data included
    """
    try:
        client = TaapiClient()
        symbol = 'BTC/USDT'

        print("\n" + "=" * 40)
        print("TESTING BULK API WITH MARKET DATA")
        print("=" * 40)

        # Test bulk query with market data
        print(f"\nTesting bulk query with market data for {symbol}...")
        bulk_data = client.get_multiple_indicators(symbol, include_market_data=True)

        print(f"Bulk response keys: {list(bulk_data.keys())}")

        # Validate all expected data is present
        expected_items = ['rsi', 'ema_14', 'sma_50', 'macd', 'bollinger', 'price', 'volume', 'candle']
        missing_items = []

        for item in expected_items:
            if item not in bulk_data:
                missing_items.append(item)
            else:
                # Show sample data for each item
                data = bulk_data[item]
                if item == 'price':
                    print(f"✓ Price: ${data.get('value', 0):,.2f}")
                elif item == 'volume':
                    vol = data.get('value', 0)
                    print(f"✓ Volume: {vol:,.2f} ({'Green' if vol > 0 else 'Red'} candle)")
                elif item == 'candle':
                    print(f"✓ Candle: O=${data.get('open', 0):,.2f}, C=${data.get('close', 0):,.2f}")
                elif item == 'rsi':
                    print(f"✓ RSI: {data.get('value', 0):.2f}")
                elif item == 'macd':
                    print(f"✓ MACD: {data.get('valueMACD', 0):.2f}")
                else:
                    print(f"✓ {item}: {data}")

        if missing_items:
            print(f"WARNING: Missing items: {missing_items}")
            return False

        print("\n✓ All technical indicators and market data fetched successfully!")
        return True

    except Exception as e:
        print(f"Bulk with market data test failed: {e}")
        return False


def run_all_tests():
    """
    Run all TAAPI tool tests including market data
    """
    load_dotenv()
    print("TAAPI Tool - Complete Testing Suite")
    print("=" * 50)

    # Check if API key is available
    api_key = os.getenv('TAAPI_API_KEY')
    if not api_key:
        print("ERROR: TAAPI_API_KEY environment variable not set")
        print("Please set your TAAPI API key: export TAAPI_API_KEY='your_key_here'")
        return False

    # Run RSI test
    success = test_rsi_fetching()
    if success:
        print("\n✓ RSI data fetching successful!")
    else:
        print("\n✗ RSI data fetching failed.")

    # Test MACD individually
    print("\n" + "=" * 40)
    print("Testing MACD Individual")
    print("=" * 40)
    test_macd_individual()

    # Test Bollinger Bands individually
    print("\n" + "=" * 40)
    print("Testing Bollinger Bands Individual")
    print("=" * 40)
    test_bollinger_individual()

    # Test market data endpoints
    market_success = test_market_data()
    if market_success:
        print("\n✓ Market data endpoints working!")
    else:
        print("\n✗ Market data endpoints failed!")

    # Test original bulk functionality
    print("\n" + "=" * 40)
    print("Testing Original Bulk Query Functionality")
    print("=" * 40)
    success_bulk = test_bulk_indicators()
    if success_bulk:
        print("\n✓ Original bulk indicator fetching successful!")
    else:
        print("\n✗ Original bulk indicator fetching failed.")

    # Test bulk API with market data
    bulk_market_success = test_bulk_with_market_data()
    if bulk_market_success:
        print("\n✓ Bulk API with market data working!")
    else:
        print("\n✗ Bulk API with market data failed!")

    print("\n" + "=" * 50)
    print("FINAL TEST RESULTS")
    print("=" * 50)
    print(f"RSI Tests: {'✓ PASSED' if success else '✗ FAILED'}")
    print(f"Individual Market Data: {'✓ PASSED' if market_success else '✗ FAILED'}")
    print(f"Original Bulk Query: {'✓ PASSED' if success_bulk else '✗ FAILED'}")
    print(f"Bulk with Market Data: {'✓ PASSED' if bulk_market_success else '✗ FAILED'}")

    all_passed = success and market_success and success_bulk and bulk_market_success
    if all_passed:
        print("\n🎉 All TAAPI tool tests passed! Full integration ready.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    run_all_tests()