import json
from datetime import datetime as dt, timezone
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


def print_messages(messages, clip=True):    
    for msg in messages:
        if isinstance(msg, AIMessage): 
            print(f"Agent: {msg.name}")
            if clip: 
                print(f"Content: {msg.content[:500]}")
            else: 
                print(f"Content: {msg.content}")
            for tool_call in msg.tool_calls: 
                print(f"Called tool: {tool_call['name']} with args {tool_call['args']}")
        if isinstance(msg, ToolMessage): 
            print(f"Tool: {msg.name}")
            print(f"Content: {msg.content}")
        if isinstance(msg, HumanMessage): 
            print(f"Human: {msg.content}")
        print("--------")
    return len(messages) 


def get_search_queries(messages):
    searches = []
    for msg in messages: 
        if isinstance(msg, AIMessage): 
            for tool_call in msg.tool_calls: 
                if tool_call['name'] == "web_search_tool":
                    searches.append(tool_call['args'])
    return searches
                
def get_technical_data(messages):
    data = []
    for msg in messages: 
        if isinstance(msg, ToolMessage): 
            if msg.name == "get_multiple_indicators": 
                data.append(json.loads(msg.content))
    return data

def create_report(investor_profile, user_question, messages, model_name="gpt-4o-mini"):
    
    report = f"Investor profile: {investor_profile}"
    report += f"User question: {user_question}\n\n"
    # datetime in UTC timezone
    current_time = dt.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report += f"Report generated on: {current_time}\n\n"

    additional_user_messages = [msg for msg in messages[1:] if isinstance(msg, HumanMessage)]
    model = ChatOpenAI(model=model_name, temperature=0)
    if additional_user_messages:
        report += "Additional user messages:\n"
        for msg in additional_user_messages:
            report += f"- {msg.content}\n"
        report += "\n"
    searches = get_search_queries(messages)
    if len(searches) > 0:
        report += "## Web searches performed:\n"
        for search in searches:
            report += f"- {search}\n"
        report += "\n"
    fear_n_greed = [msg for msg in messages if isinstance(msg, ToolMessage) and msg.name == "get_fear_greed_index"]
    if len(fear_n_greed) > 0:
        report += f"## Fear and Greed Index data:\n{fear_n_greed[-1].content}\n\n"
    technical_data = get_technical_data(messages)
    if len(technical_data) > 0:
        report += "## Technical analysis data retrieved:\n"
        for data in technical_data:
            report += f"- {data}\n"
        report += "\n"

    report += "## Technical analysis: \n"
    tech_analysis_msgs = [msg for msg in messages if isinstance(msg, AIMessage) and msg.name == "tech_analysis_expert"
                          and len(msg.content) > 100]
    if tech_analysis_msgs:
        report += tech_analysis_msgs[-1].content + "\n\n"

    report += "## Web sentiment analysis: \n"
    web_sentiment_msgs = [msg for msg in messages if isinstance(msg, AIMessage) and msg.name == "web_sentiment_expert"
                          and len(msg.content) > 100]
    if web_sentiment_msgs:
        report += web_sentiment_msgs[-1].content + "\n\n"
    
    report += "## Final recommendation and reasoning:\n"
    final_reco = messages[-1]
    report += final_reco.content + "\n\n"
    return report