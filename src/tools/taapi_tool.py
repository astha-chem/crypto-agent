"""
TAAPI.IO API Client for Technical Analysis Indicators
Phase 1: Basic RSI implementation with authentication and error handling
"""
import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from ..utils.logging_config import setup_logger

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
                               exchange: str = "binance",
                               interval: str = "1h") -> Dict[str, Any]:
        """
        Get multiple indicators in a single bulk request using TAAPI bulk query

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (default: 'binance')
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w)

        Returns:
            Dictionary containing all indicator values
            Example: {
                "rsi": {"value": 32.5},
                "ema_14": {"value": 43250.5},
                "sma_50": {"value": 41500.2},
                "macd": {"valueMACD": 123.45, "valueMACDSignal": 120.30, "valueMACDHist": 3.15},
                "bollinger": {"valueUpperBand": 45800.0, "valueMiddleBand": 43250.0, "valueLowerBand": 40700.0}
            }
        """
        # TAAPI bulk query payload format
        payload = {
            "secret": self.api_key,
            "construct": {
                "exchange": exchange,
                "symbol": symbol,
                "interval": interval,
                "indicators": [
                    {"indicator": "rsi", "period": 14},
                    {"indicator": "ema", "period": 14},
                    {"indicator": "sma", "period": 50},
                    {"indicator": "macd"},
                    {"indicator": "bbands", "period": 20, "stddev": 2.0}
                ]
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

                        if indicator_name == 'rsi':
                            parsed_response['rsi'] = result
                        elif indicator_name == 'ema' and '_14_' in item_id:
                            parsed_response['ema_14'] = result
                        elif indicator_name == 'sma' and '_50_' in item_id:
                            parsed_response['sma_50'] = result
                        elif indicator_name == 'macd':
                            parsed_response['macd'] = result
                        elif indicator_name == 'bbands':
                            parsed_response['bollinger'] = result

            return parsed_response

        except Exception as e:
            logger.warning(f"Bulk query failed, falling back to individual requests: {e}")

            return {
                'rsi': self.get_rsi(symbol, exchange, interval),
                'ema_14': self.get_ema(symbol, 14, exchange, interval),
                'sma_50': self.get_sma(symbol, 50, exchange, interval),
                'macd': self.get_macd(symbol, exchange, interval),
                'bollinger': self.get_bollinger_bands(symbol, exchange, interval)
            }