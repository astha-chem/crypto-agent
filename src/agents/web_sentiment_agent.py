"""
Simple Web Sentiment Agent using LangChain
"""
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from src.tools.fear_greed_tool import get_fear_greed_index
from src.tools.playwright_tool import WebScrapingTool
import os 
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
load_dotenv()


@tool("web_search_tool")
def web_search_tool(search_query: str, news_only: bool = False, limit_last_day: bool = False,
                    metadata: bool = False):
    """
    Search Google for information using the Serper API.

    Args:
        search_query: The search terms to look for (e.g., "Bitcoin price analysis", "crypto market sentiment")
        news_only: If True, search only news articles. If False, search all web content
        limit_last_day: If True, limit results to past 24 hours. If False, search past week
        metadata: If True, return detailed metadata (links, snippets). If False, return summary text only. 

    Returns:
        Search results - either detailed metadata or summary text depending on metadata parameter

    Examples:
        - For recent Bitcoin news: web_search_tool("Bitcoin news", news_only=True, limit_last_day=True)
        - For crypto sentiment: web_search_tool("crypto market sentiment reddit twitter", metadata=True)
        - For general analysis: web_search_tool("BTC technical analysis")
    """
    if limit_last_day: 
        time_kw = "qdr:d"
    else: 
        time_kw = "qdr:w"

    if news_only: 
        search_tool = GoogleSerperAPIWrapper(serper_api_key=os.getenv("serper_api_key"),
            k=10,  # Number of results
            gl="us",
            hl="en",
            type="news", 
            tbs=time_kw)
    else: 
        search_tool = GoogleSerperAPIWrapper(serper_api_key=os.getenv("serper_api_key"),
            k=10,  # Number of results
            gl="us",
            hl="en",
            tbs=time_kw)
    if metadata: 
        return search_tool.results(search_query)
    else: 
        return search_tool.run(search_query)


web_sentiment_system_prompt = """You are a professional cryptocurrency sentiment analyst. Your job is to analyze market sentiment from various web sources and provide actionable insights.
When analyzing sentiment data, consider:
1. Fear & Greed Index levels and interpretation
2. News sentiment (positive/negative headlines, regulatory news)
3. Social media sentiment and discussions (Twitter, Reddit, forums)
4. Institutional activity (whale movements, corporate adoption)
5. Market narrative and trending topics

EXAMPLE SEARCH QUERIES (do not include dates - set "limit_last_day" to True for most recent results. By default, we filter to last week.):
- "Bitcoin price today breaking news"
- "Bitcoin whale movement large transactions"
- "BTC institutional buying selling activity"
- "site:reddit.com/r/CryptoCurrency Bitcoin pump dump",
- "Bitcoin Twitter sentiment reddit discussion"
- "cryptocurrency fear uncertainty doubt FUD"

ANALYSIS FRAMEWORK:
Always provide:
- Overall market sentiment (extreme fear/fear/neutral/greed/extreme greed)
- Key sentiment drivers by category:
  * Institutional/Whale activity
  * News/Media sentiment
  * Social media sentiment
- Sentiment trend direction (improving/deteriorating/stable)
- Risk/opportunity assessment
- Confidence level in your sentiment analysis

Use at least 5 searches to build a comprehensive view before providing your final analysis."""

web_sentiment_default_user_input = "Analyze current Bitcoin sentiment. Check fear & greed index, search for recent BTC news, and specifically search for social sentiment as well. You can make upto 5 searches. Provide a comprehensive report based on your searches."
# tools = fgi_tools + news_search_tools + web_search_tools + navigate_web_page_tools

web_sentiment_tools = [get_fear_greed_index, web_search_tool]

def run_new_web_sentiment_agent_node(thread_id: str, user_input: str = None, model: str = "openai:gpt-4o-mini", 
                                     messages=None): 
    web_sentiment_tools = [get_fear_greed_index, web_search_tool]
    # Initialize chat model
    model = init_chat_model("openai:gpt-4o-mini")
    # Create the agent
    agent_executor = create_react_agent(model, tools, prompt=web_sentiment_system_prompt)
    # Test question
    config = {"configurable": {"thread_id": thread_id}}
    input_message = {
        "role": "user",
        "content": web_sentiment_default_user_input if user_input is None else user_input
    }
    response = agent_executor.invoke({"messages": [input_message]}, config)
    for message in response["messages"]:
        message.pretty_print()
    return response, thread_id



if __name__ == "__main__":
    response, thread_id = run_new_web_sentiment_agent_node(thread_id="test_web_sentiment_1", user_input="Is this a good time to buy Bitcoin? ")
    print("Final message: ", response['messages'][-1])
    # tool_calls = [msg for msg in response['messages'] if isinstance(msg, ToolMessage)]
    # for tool_call in tool_calls:
    #     print("Tool call: ", tool_call)
    

