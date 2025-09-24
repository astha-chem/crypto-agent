"""
TAAPI.IO API Client for Technical Analysis Indicators
Phase 1: Basic RSI implementation with authentication and error handling
"""
import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from src.utils.logging_config import setup_logger

logger = setup_logger(__name__, 'taapi.log')

class TaapiClient:
    """
    Client for TAAPI.IO Technical Analysis API
    Supports fetching technical indicators for cryptocurrency trading pairs
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TAAPI client

        Args:
            api_key: TAAPI.IO API key. If None, will try to get from TAAPI_API_KEY env var
        """
        self.api_key = api_key or os.getenv('TAAPI_API_KEY')
        if not self.api_key:
            raise ValueError("TAAPI API key is required. Set TAAPI_API_KEY environment variable or pass api_key parameter.")

        self.base_url = "https://api.taapi.io"
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make authenticated request to TAAPI API

        Args:
            endpoint: API endpoint (e.g., 'rsi')
            params: Query parameters

        Returns:
            JSON response as dictionary

        Raises:
            requests.RequestException: On API request failures
            ValueError: On invalid response data
        """
        # Add API key to parameters
        params['secret'] = self.api_key

        url = f"{self.base_url}/{endpoint}"

        try:
            # Create sanitized params for logging (hide API key)
            log_params = {k: v for k, v in params.items() if k != 'secret'}
            log_params['secret'] = '[HIDDEN]'
            logger.info(f"Making request to {endpoint} with params: {log_params}")

            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Successfully fetched {endpoint} data")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {endpoint}: {e}")
            raise
        except ValueError as e:
            logger.error(f"Failed to parse JSON response for {endpoint}: {e}")
            raise

    def get_rsi(self,
                symbol: str,
                exchange: str = "binance",
                interval: str = "1h",
                period: int = 14) -> Dict[str, Any]:
        """
        Get RSI (Relative Strength Index) for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)
            period: RSI calculation period (default: 14)

        Returns:
            Dictionary containing RSI value and metadata
            Example: {"value": 32.5}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval,
            'period': period
        }

        return self._make_request('rsi', params)

    def get_ema(self,
                symbol: str,
                period: int = 14,
                exchange: str = "binance",
                interval: str = "1h") -> Dict[str, Any]:
        """
        Get EMA (Exponential Moving Average) for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            period: EMA calculation period (default: 14)
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)

        Returns:
            Dictionary containing EMA value
            Example: {"value": 43250.5}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('ema', params)

    def get_sma(self,
                symbol: str,
                period: int = 50,
                exchange: str = "binance",
                interval: str = "1h") -> Dict[str, Any]:
        """
        Get SMA (Simple Moving Average) for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            period: SMA calculation period (default: 50)
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)

        Returns:
            Dictionary containing SMA value
            Example: {"value": 41500.2}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('sma', params)

    def get_macd(self,
                 symbol: str,
                 exchange: str = "binance",
                 interval: str = "1h") -> Dict[str, Any]:
        """
        Get MACD (Moving Average Convergence Divergence) for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)

        Returns:
            Dictionary containing MACD values
            Example: {"valueMACD": 123.45, "valueMACDSignal": 120.30, "valueMACDHist": 3.15}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval
        }
        return self._make_request('macd', params)

    def get_bollinger_bands(self,
                           symbol: str,
                           exchange: str = "binance",
                           interval: str = "1h",
                           period: int = 20,
                           stddev: float = 2.0) -> Dict[str, Any]:
        """
        Get Bollinger Bands for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)
            period: Bollinger Bands period (default: 20)
            stddev: Standard deviation multiplier (default: 2.0)

        Returns:
            Dictionary containing Bollinger Bands values
            Example: {"valueUpperBand": 45800.0, "valueMiddleBand": 43250.0, "valueLowerBand": 40700.0}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval,
            'period': period,
            'stddev': stddev
        }
        return self._make_request('bbands', params)

    def get_price(self,
                  symbol: str,
                  exchange: str = "binance",
                  interval: str = "1h") -> Dict[str, Any]:
        """
        Get current price for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)

        Returns:
            Dictionary containing current price
            Example: {"value": 43250.5}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval
        }
        return self._make_request('price', params)

    def get_volume(self,
                   symbol: str,
                   exchange: str = "binance",
                   interval: str = "1h") -> Dict[str, Any]:
        """
        Get volume data for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)

        Returns:
            Dictionary containing volume data
            Example: {"value": 12345.67} (positive for green candles, negative for red)
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval
        }
        return self._make_request('volume', params)

    def get_candle(self,
                   symbol: str,
                   exchange: str = "binance",
                   interval: str = "1h",
                   backtrack: int = 0) -> Dict[str, Any]:
        """
        Get OHLCV candle data for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)
            backtrack: Number of candles back (0 = current, 1 = previous, etc.)

        Returns:
            Dictionary containing OHLCV data
            Example: {"timestampOpen": 1234567890, "open": 43000, "high": 43500, "low": 42800, "close": 43250, "volume": 12345.67}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval,
            'backtrack': backtrack
        }
        return self._make_request('candle', params)

    def get_candles(self,
                    symbol: str,
                    exchange: str = "binance",
                    interval: str = "1h",
                    period: int = 10) -> Dict[str, Any]:
        """
        Get multiple OHLCV candles for a trading pair

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)
            period: Number of candles to retrieve (default: 10)

        Returns:
            Dictionary containing array of OHLCV data
            Example: {"data": [{"timestampOpen": 1234567890, "open": 43000, ...}, ...]}
        """
        params = {
            'exchange': exchange,
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('candles', params)

    def _make_bulk_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make POST request to TAAPI bulk endpoint

        Args:
            payload: JSON payload for bulk request

        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}/bulk"

        try:
            # Create sanitized payload for logging (hide API key)
            log_payload = payload.copy()
            log_payload['secret'] = '[HIDDEN]'
            logger.info(f"Making bulk POST request with payload: {log_payload}")

            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Successfully fetched bulk data")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Bulk API request failed: {e}")
            raise
        except ValueError as e:
            logger.error(f"Failed to parse bulk JSON response: {e}")
            raise

    def get_multiple_indicators(self,
                               symbol: str,
                               interval: str = "1d",
                               exchange: str = "binance",
                               ) -> Dict[str, Any]:
        """
        Get comprehensive technical analysis indicators and market data in a single optimized API call.

        This function retrieves all essential technical indicators and market data needed for cryptocurrency
        analysis using TAAPI.io's bulk query API. It combines multiple data points into one efficient request
        to minimize API usage and latency.

        TECHNICAL INDICATORS INCLUDED (Fixed Parameters):

        1. RSI (Relative Strength Index) - Period: 14
           - Momentum oscillator measuring speed and change of price movements
           - Returns: {"value": float} - Range 0-100, <30 = oversold, >70 = overbought

        2. EMA (Exponential Moving Average) - Period: 14
           - Trend-following indicator giving more weight to recent prices
           - Returns: {"value": float} - Current EMA value in quote currency

        3. SMA (Simple Moving Average) - Period: 50
           - Trend indicator using arithmetic mean of closing prices
           - Returns: {"value": float} - Current SMA value in quote currency

        4. MACD (Moving Average Convergence Divergence) - Standard settings (12,26,9)
           - Momentum indicator showing relationship between two moving averages
           - Returns: {
               "valueMACD": float,         # MACD line (12-period EMA minus 26-period EMA)
               "valueMACDSignal": float,   # Signal line (9-period EMA of MACD line)
               "valueMACDHist": float      # Histogram (MACD line minus Signal line)
             }

        5. Bollinger Bands - Period: 20, Standard Deviation: 2.0
           - Volatility indicator with upper and lower bands around moving average
           - Returns: {
               "valueUpperBand": float,    # Upper band (SMA + 2*standard deviation)
               "valueMiddleBand": float,   # Middle band (20-period SMA)
               "valueLowerBand": float     # Lower band (SMA - 2*standard deviation)
             }

        MARKET DATA INCLUDED:

        6. Current Price
           - Real-time price of the trading pair
           - Returns: {"value": float} - Current price in quote currency

        7. Volume
           - Trading volume for current candle period
           - Returns: {"value": float} - Positive for green candles, negative for red candles

        8. OHLCV Candle Data
           - Complete candlestick information for current period
           - Returns: {
               "open": float,          # Opening price
               "high": float,          # Highest price
               "low": float,           # Lowest price
               "close": float,         # Closing price
               "volume": float,        # Trading volume
               "timestampOpen": int    # Unix timestamp of candle open
             }

        Args:
            symbol (str): Trading pair in format 'BASE/QUOTE' (e.g., 'BTC/USDT', 'ETH/USDT')
                         Symbol must be uppercase and supported by the specified exchange

            exchange (str, optional): Cryptocurrency exchange name. Defaults to 'binance'.
                                    Supported exchanges: binance, binancefutures, coinbase, kraken, etc.

            interval (str, optional): Time interval for analysis. Defaults to '1d'.
                                    Supported intervals:
                                    - '1m' (1 minute) - High frequency trading
                                    - '5m' (5 minutes) - Scalping strategies
                                    - '15m' (15 minutes) - Short-term analysis
                                    - '30m' (30 minutes) - Intraday analysis
                                    - '1h' (1 hour) - Hourly analysis
                                    - '4h' (4 hours) - Swing trading
                                    - '1d' (1 day) - Daily analysis (recommended for most strategies)
                                    - '1w' (1 week) - Weekly long-term analysis

        Returns:
            Dict[str, Any]: Dictionary containing all technical indicators and market data with keys:
                - 'rsi': RSI indicator data
                - 'ema': EMA (14-period) indicator data
                - 'sma': SMA (50-period) indicator data
                - 'macd': MACD indicator data with line, signal, and histogram
                - 'bbands': Bollinger Bands data with upper, middle, lower bands
                - 'price': Current price data
                - 'volume': Volume data for current candle
                - 'candle': Complete OHLCV candle data

            Returns empty dict {} if API request fails or rate limit exceeded (429 error).

        Example Usage:
            >>> client = TaapiClient()
            >>> data = client.get_multiple_indicators('BTC/USDT', interval='1h')
            >>> current_price = data['price']['value']
            >>> rsi_value = data['rsi']['value']
            >>> macd_line = data['macd']['valueMACD']
            >>> upper_band = data['bbands']['valueUpperBand']

        Note:
            - All price values are in the quote currency (e.g., USDT for BTC/USDT)
            - This function optimizes API usage by fetching all data in one bulk request
            - Rate limiting: Returns empty dict if 429 (Too Many Requests) error occurs
            - Indicators use standard settings optimized for most trading strategies
            - Market data reflects the current state at the time of the API call
        """
        # Base indicators
        indicators = [
            {"indicator": "rsi", "period": 14},
            {"indicator": "ema", "period": 14},
            {"indicator": "sma", "period": 50},
            {"indicator": "macd"},
            {"indicator": "bbands", "period": 20, "stddev": 2.0}
        ]

        # Add market data indicators if requested
        indicators.extend([
            {"indicator": "price"},
            {"indicator": "volume"},
            {"indicator": "candle"}
        ])

        # TAAPI bulk query payload format
        payload = {
            "secret": self.api_key,
            "construct": {
                "exchange": exchange,
                "symbol": symbol,
                "interval": interval,
                "indicators": indicators
            }
        }

        try:
            bulk_response = self._make_bulk_request(payload)
            parsed_response = {}

            if isinstance(bulk_response, dict) and 'data' in bulk_response:
                for item in bulk_response['data']:
                    if isinstance(item, dict):
                        indicator_name = item.get('indicator', '')
                        result = item.get('result', {})
                        item_id = item.get('id', '')
                        parsed_response[indicator_name] = result
            return parsed_response

        except Exception as e:
            logger.warning(f"Bulk query failed,: {e}")
            if "429" in e: 
                logger.warning(f"Bulk query failed. Hit API limit. Try again in 15s.")
            return {}
        
       

if __name__ == "__main__": 
    from dotenv import load_dotenv
    load_dotenv()
    client = TaapiClient()
    symbol = 'BTC/USDT'
    print("Testing bulk indicator fetch for BTC/USDT...")
    bulk_data = client.get_multiple_indicators('BTC/USDT')
    print(bulk_data)

    

