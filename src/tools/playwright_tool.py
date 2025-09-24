import asyncio
import nest_asyncio
from langchain_core.tools import BaseTool
from langchain_community.tools.playwright import ExtractTextTool
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",   },
)
from pydantic import BaseModel, Field
from typing import Optional

nest_asyncio.apply()

async def extract_text_from_url(url):
    async_browser = create_async_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    tools = toolkit.get_tools()

    print("Available tools:", [tool.name for tool in tools])
    tools_by_name = {tool.name: tool for tool in tools}

    print("Navigating to URL...")
    await tools_by_name["navigate_browser"].arun({"url": url})

    print("Extracting text from current page...")
    result = await tools_by_name["extract_text"].arun({})

    print(f"Result type: {type(result)}")
    print(f"Result length: {len(str(result)) if result else 0}")
    return result[:5000] if result else ""

class WebScrapingInput(BaseModel):
    url: str = Field(description="The URL to scrape text from")

class WebScrapingTool(BaseTool):
    name: str = "web_scraping"
    description: str = "Extract text content from web pages using Playwright browser automation"
    args_schema: type[BaseModel] = WebScrapingInput

    def _run(self, url: str) -> str:
        """Synchronous wrapper for the async function"""
        try:
            return asyncio.run(extract_text_from_url(url))
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"

    async def _arun(self, url: str) -> str:
        """Async version"""
        try:
            return await extract_text_from_url(url)
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    import pprint
    # Create the tool instance
    web_scraping_tool = WebScrapingTool()
    result = web_scraping_tool.run({"url": "https://python.langchain.com/docs/tutorials/agents/"})
    pprint.pprint(result)
