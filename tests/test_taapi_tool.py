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


if __name__ == "__main__":
    run_all_tests()