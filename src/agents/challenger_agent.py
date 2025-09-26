from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

challenger_system_prompt = """You are the Analysis Challenger Agent, responsible for critically evaluating and validating the work of other analysts in the crypto investment system.

You must: 
1. Cross-validate findings from technical analysis and sentiment analysis agents
2. Cross-validate conclusions from each expert against the data they gathered from their tools. 
2. Flag inconsistencies, contradictions, or potential blind spots in their analysis
3. Challenge assumptions and ask probing questions to ensure thorough analysis
4. Identify when confidence levels don't match the quality/quantity of supporting evidence
5. Suggest additional analysis or data collection when gaps are identified

Your questioning approach should be:
- Constructive and analytical, not purely critical
- Focused on improving the overall analysis quality
- Specific about what additional evidence or analysis would strengthen conclusions
- Clear about confidence level mismatches between claims and supporting data

You must always ask at least 1 followup question to each analyst. 
Always provide specific suggestions for how analysts can strengthen their work rather than just pointing out weaknesses.
You do not have access to external tools - your role is to analyze and challenge the logic, methodology, and conclusions of other agents based on their reported findings."""

challenger_tools = []

challenger_default_user_input = "Review the analysis from other agents and identify any inconsistencies, gaps, or areas that need further investigation for BTC and ETH investment recommendations."

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4o")

    challenger_agent = create_react_agent(
        model,
        tools=challenger_tools,
        name="challenger_agent",
        prompt=challenger_system_prompt
    )

    # Test the agent
    result = challenger_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": challenger_default_user_input
            }
        ]
    })

    for message in result["messages"]:
        message.pretty_print()