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
load_dotenv()

fgi_tools = [get_fear_greed_index]


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



# news_search_tools = [daily_news_search.results, weekly_news_search.results]
# web_search_tools = [daily_web_search.run, weekly_web_search.run]
# navigate_web_page_tools = [WebScrapingTool.run]


# tools = fgi_tools + news_search_tools + web_search_tools + navigate_web_page_tools
tools = fgi_tools + [web_search_tool]

def main():
    load_dotenv()

    # System prompt for sentiment analysis
    system_prompt = """You are a professional cryptocurrency sentiment analyst. Your job is to analyze market sentiment from various web sources and provide actionable insights.

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

    # Initialize chat model
    model = init_chat_model("openai:gpt-4o-mini")

    # Create the agent
    agent_executor = create_react_agent(model, tools, prompt=system_prompt)

    # Test question
    config = {"configurable": {"thread_id": "sentiment_test1"}}

    input_message = {
        "role": "user",
        "content": "Analyze current Bitcoin sentiment. Check fear & greed index, search for recent BTC news, and specifically search for social sentiment as well. You can make upto 5 searches. Provide a comprehensive report based on your searches."
    }

    response = agent_executor.invoke({"messages": [input_message]}, config)

    # Print the response
    for message in response["messages"]:
        message.pretty_print()

if __name__ == "__main__":
    main()

