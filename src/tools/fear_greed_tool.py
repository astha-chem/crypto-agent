import requests
from langchain.tools import Tool
from typing import Dict, Any


def get_fear_greed_index() -> str:
    """Get current Fear and Greed Index with 7-day trend analysis"""
    try:
        # Get historical data for trend analysis (7 days)
        response = requests.get("https://api.alternative.me/fng/?limit=7", timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and len(data['data']) > 0:
            # Current value (most recent)
            current = data['data'][0]
            current_value = int(current['value'])
            classification = current['value_classification']
            timestamp = current['timestamp']

            # Calculate trend analysis
            values = [int(item['value']) for item in data['data']]
            avg_value = sum(values) / len(values)

            # Determine trend
            if len(values) >= 2:
                trend = "rising" if values[0] > values[-1] else "falling" if values[0] < values[-1] else "stable"
            else:
                trend = "stable"

            analysis = f"""Fear & Greed Index Analysis (7 days):
Latest Value: {current_value} ({classification})
Average Value: {avg_value:.1f}
Trend: {trend}
Data points: {len(values)}"""

            return analysis
        else:
            return "Fear & Greed Index: Unable to retrieve data"

    except Exception as e:
        return f"Fear & Greed Index: Error - {str(e)}"


def create_fear_greed_tool():
    """Create Fear and Greed Index tool"""
    return Tool(
        name="fear_greed_index",
        description=(
            "Get Fear and Greed Index (0-100 scale) current value and analysis."
            "Values: 0-24 = Extreme Fear, 25-49 = Fear, 50-74 = Greed, 75-100 = Extreme Greed. "
            "Use for market sentiment analysis."
        ),
        func=lambda x: get_fear_greed_index(),
    )


def main():
    """Test the Fear and Greed tool"""
    print("Testing Fear and Greed Index Tool...")
    tool = create_fear_greed_tool()
    result = tool.run("")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()