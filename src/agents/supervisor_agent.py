from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

from src.agents.technical_analysis_agent import tech_analysis_tools, tech_analysis_system_prompt, tech_analysis_default_user_input
from src.agents.web_sentiment_agent import web_sentiment_tools, web_sentiment_system_prompt, web_sentiment_default_user_input
from src.agents.challenger_agent import challenger_tools, challenger_system_prompt, challenger_default_user_input

import json 

load_dotenv()
openai_mini_model = ChatOpenAI(model="gpt-4o-mini")

openai_model = ChatOpenAI(model="gpt-4o")
# anthropic_model = ChatAnthropic(model="claude-sonnet-4-20250514") 
deepseek_model = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.1)

tech_analysis_agent = create_react_agent(
    openai_model,
    tools=tech_analysis_tools,
    name="tech_analysis_expert",
    prompt=tech_analysis_system_prompt
)

web_sentiment_agent = create_react_agent(
    openai_mini_model,
    tools=web_sentiment_tools,
    name="web_sentiment_expert",
    prompt=web_sentiment_system_prompt
)

challenger_agent = create_react_agent(
    openai_model,
    tools=challenger_tools,
    name="challenger_expert",
    prompt=challenger_system_prompt
)

supervisor_crypto_analyst_prompt = """You are the Lead Crypto Analyst, responsible for providing actionable recommendations on cryptocurrency investments
        focusing on BTC and ETH only. You have access to three expert agents: web_sentiment_expert, tech_analysis_expert, and challenger_expert.
        Use the web_sentiment_expert for analyzing the market sentiment from web sources, social media and news reports on the market and whale activity.
        Use tech_analysis_expert for technical analysis using indicators.
        Use challenger_expert to validate and cross-check analysis from other agents, identify inconsistencies, and ensure thorough evaluation.

        Typical workflow:
        1. Call both sentiment and technical analysis agents to gather initial data
        2. Use challenger_expert to review each analyst's findings against the data they accessed and identify any gaps or inconsistencies
        3. If challenger raises valid concerns, have the relevant agents do additional analysis
        4. Make final recommendation only after challenger validation

        Don't make up information - if you don't have enough data, do further analysis. 
        Always think step-by-step and plan your approach before calling the agents.
        You can call the agents multiple times if needed, but avoid excessive calls.
        Your final output should be a concise investment recommendation (buy/sell/hold) for BTC and ETH, along with key reasons and confidence level.
        """

# Create supervisor workflow
workflow = create_supervisor(
    [tech_analysis_agent, web_sentiment_agent, challenger_agent],
    model=openai_mini_model,
    prompt=(
        supervisor_crypto_analyst_prompt
    ),
    output_mode="full_history"
)

# Compile and run
app = workflow.compile()

with open("/Users/asthagarg/repos/crypto-agent/user_profiles.json", "r") as f: 
    user_profiles = json.loads(f.read())

investor_profile = user_profiles['aggressive_young']

question_template = """User profile: {investor_profile}.
User question: {question}"""


user_question = "Crypto market seems to be falling. Should I buy more? "
config = {"configurable": {"thread_id": "supervisor_test_1"}}
result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": question_template.format(investor_profile=investor_profile, question=user_question)
        }
    ]
}, 
config)

for message in result["messages"]:
    message.pretty_print()


print("Second invocation with follow-up question now.")

result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Thanks for your analysis. But I just lost my job and need to be very conservative with my money now. Should I still proceed with your recommendation? "
        },  
    ]
}, config)

for message in result["messages"]:
    message.pretty_print()