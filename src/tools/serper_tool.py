import os
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import Tool
from dotenv import load_dotenv

load_dotenv()


def create_serper_search_tool():
    """Create a Serper search tool using LangChain's built-in implementation"""

    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY environment variable is required")

    search = GoogleSerperAPIWrapper(
        serper_api_key=api_key,
        k=10,  # Number of results
        gl="us",  # Country
        hl="en",  # Language
    )

    return Tool(
        name="serper_search",
        description=(
            "Search for cryptocurrency news, articles, and web content. "
            "Use this tool to find recent news about Bitcoin, Ethereum, regulations, "
            "market sentiment, and other crypto-related topics. "
            "Input should be a search query string."
        ),
        func=search.run,
    )


def create_serper_news_tool():
    """Create a Serper news-specific tool using LangChain's built-in implementation"""

    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY environment variable is required")

    news_search = GoogleSerperAPIWrapper(
        serper_api_key=api_key,
        k=15,  # Number of results
        gl="us",
        hl="en",
        type="news",  # Specifically search news
        tbs="qdr:w"   # Results from past week
    )

    return Tool(
        name="serper_news",
        description=(
            "Search specifically for cryptocurrency news articles. "
            "Use this tool to find breaking news, regulatory updates, "
            "market announcements, and recent developments in crypto. "
            "Input should be a news search query."
        ),
        func=news_search.run,
    )


def main():
    """Test the Serper tools with sample queries"""
    print("Testing Serper Tools...")
    print("=" * 50)

    try:
        # Test general search tool
        print("\n1. Testing General Search Tool:")
        search_tool = create_serper_search_tool()
        search_result = search_tool.run("Bitcoin ETF approval SEC")
        print(f"Query: 'Bitcoin ETF approval SEC'")
        print(f"Result: {search_result[:500]}...")

        print("\n" + "-" * 50)

        # Test news search tool
        print("\n2. Testing News Search Tool:")
        news_tool = create_serper_news_tool()
        news_result = news_tool.run("Ethereum price analysis")
        print(f"Query: 'Ethereum price analysis'")
        print(f"Result: {news_result[:500]}...")

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set SERPER_API_KEY in your .env file")
    except Exception as e:
        print(f"Error testing tools: {e}")


if __name__ == "__main__":
    main()