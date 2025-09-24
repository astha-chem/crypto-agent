"""
Simple Technical Analysis Agent using LangChain
"""
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from src.tools.taapi_tool import TaapiClient
from dotenv import load_dotenv

def main():
    load_dotenv()
    # System prompt for technical analysis
    system_prompt = """You are a professional cryptocurrency technical analyst. Your job is to analyze technical indicators and provide actionable investment insights.

When analyzing technical data, consider:
1. Trend direction (moving averages, price action)
2. Momentum (RSI, MACD)
3. Support/resistance levels (Bollinger Bands, price levels)
4. Volume confirmation
5. Risk assessment

Always provide:
- Clear interpretation of technical indicators
- Market sentiment (bullish/bearish/neutral)
- Specific price levels to watch
- Risk management recommendations
- Confidence level in your analysis"""

    # Initialize tools
    taapi_client = TaapiClient()
    tools = [taapi_client.get_multiple_indicators]

    # Initialize chat model
    model = init_chat_model("openai:gpt-4o-mini")

    # Create the agent
    agent_executor = create_react_agent(model, tools, prompt=system_prompt)

    # Test question
    config = {"configurable": {"thread_id": "test1"}}
    input_message = {"role": "user", "content": "Analyze BTC/USDT on daily timeframe. Provide comprehensive technical analysis with actionable insights."}

    response = agent_executor.invoke({"messages": [input_message]}, config)

    # Print the response
    for message in response["messages"]:
        message.pretty_print()

    config = {"configurable": {"thread_id": "test1"}}
    print("Now adding a human-in-the-loop response on the 1day analysis : test1")
    input_message = {"role": "user", "content": "Given the 1 day analysis you did already, can you compare, confirm, contrast against a 4h analysis?"}
    messages = response["messages"]
    messages.append(input_message)
    response = agent_executor.invoke({"messages": messages}, config)

    # Print the response
    for message in response["messages"]:
        message.pretty_print()

    # to start a new chain, create a new thread instead of appending messages like this. 



if __name__ == "__main__":
    main()