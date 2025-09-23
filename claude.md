Multi-Agent Crypto Investment Analyst
You are an expert at building multi-agent trading agents. Also, you have deep knowledge of Crypto trading. You are going to assist me with building a multi-agent AI system that analyzes cryptocurrency data and generates investment reports with actionable recommendations.

The system will feature specialized agents working together to reach investment decisions, with human-in-the-loop design enabling users to provide input, and maintain oversight throughout the analysis process. 

## Agents in the multi-agent system
Planning & Reasoning
Demonstrate each agent's ability to plan its analysis approach. Show clear reasoning chains for investment decisions. Include self-reflection or validation steps.

1. User-interface agent
- job scope: handle user-interaction, plan tasks and assign to different agents. 
- reports to: user 
- direct reports: Intelligence fusion agent, Action-recommender agent
- tools: None

2. Intelligence fusion agent
- job scope: Synthesizes knowledge and intelligence based on analysis from multiple sources. 
- reports to: User-interface agent
- direct reports: All analysis agents, Analysis challenger agent 
- tools: None

3. Action-recommender agent 
- job scope: Generates action recommendations for users based on analysis done by intelligence fusion agent, user-profile, and user-requests. 
- reports to: User-interface agent
- direct reports: None
- tools: None

4. Analysis challenger Agent
- job scope: Helps sanity check or evaluate the work of any analyst. Cross-validates findings and flags inconsistencies.
- reports to: Intelligence fusion agent
- direct reports: None
- tools: None
- testing strategy: Compare outputs against known historical events, flag confidence conflicts

5. Technical Analysis Agent
- job scope: Analyzes price data, technical indicators, volume patterns, and market trends
- reports to: Intelligence fusion agent
- direct reports: None
- tools: CoinGecko API
- testing strategy: Full backtesting with historical OHLC data, validate against known technical patterns

6. On-Chain Analysis Agent
- job scope: Tracks whale movements, exchange flows, large transactions, and blockchain activity
- reports to: Intelligence fusion agent  
- direct reports: None
- tools: Blockchair API (Bitcoin), Etherscan API (Ethereum)
- testing strategy: Partial backtesting with historical transaction data, validate against known whale events

7. DeFi Fundamentals Analysis Agent
- job scope: Monitors DeFi protocol health, TVL changes, yield trends, and ecosystem growth
- reports to: Intelligence fusion agent
- direct reports: None
- tools: DeFiLlama API
- testing strategy: Good backtesting with historical TVL data, validate against DeFi sector movements

8. Sentiment Fusion Agent
- job scope: Combines market sentiment, news intelligence, and social sentiment into unified sentiment analysis
- reports to: Intelligence fusion agent
- direct reports: None
- tools: Serper API, Fear & Greed Index, Reddit API
- testing strategy: Won't be back-tested but we will use synthetic reports as proxy of this agent's output when testing other agents

## Tools 
Focus on ETH/BTC
  1. CoinGecko API (price/market data)
  2. Serper API (search/news)
  3. DeFiLlama API (DeFi analysis)
  4. Fear & Greed Index (sentiment)
  5. Reddit API (social sentiment)
  6. Blockchair API (Bitcoin on-chain)
  7. Etherscan API (Ethereum on-chain)

Consider MCP servers, function calling, or custom tool implementations
Show effective orchestration of multiple tools. 

## Human-in-the-Loop Design

User profile is provided at the start through a user_profile json spec. Example profiles to use during testing are in user_profiles.json 

### Bot initiated questions asking for human input. 
Validation & Override

  Sanity checks:
  - "This recommendation differs significantly from last week. Confirm you want this strategy change?"
  - "System confidence is only 60%. Would you like a second analysis or manual review?"

Real-Time Adjustments

  Breaking news responses:
  - "Breaking: SEC Bitcoin ETF news. Pause current analysis and reassess? Y/N"
  - "Whale movement detected during analysis. Refresh data or continue with current dataset?"

Suggesting changes to user settings: 
  - "System detected 3 strong buy signals, but your monthly budget is exceeded. Increase budget or wait for next month?"

### User follow-ups 
Understanding existing analysis 
- User: You have suggested selling BTC 50% with a confidence of 75%. What could go wrong if I took your suggestion? 

### What-if scenarios from the user
- User: What would you recommend if my risk level was conservative instead of medium risk? 

### User adding new information
- User: I know from an external source that the sentiment on BTC is bad. How does that change your analysis? 
- User: Given your analysis, what would I do as per the Dollar Cost Averaging strategy? 


## What kind of information could we glean? 
High-Confidence Buy Signals:

  - Whale accumulation (Blockchair/Etherscan) + oversold technical (CoinGecko) + positive news (Serper) + bullish social sentiment (Reddit)
  - Exchange outflows (on-chain) + DeFi TVL growth (DeFiLlama) + Fear index below 25 (extreme fear = opportunity)

High-Confidence Sell Signals:

  - Whale distribution (large wallet sales) + exchange inflows + negative regulatory news + social FOMO peaks (euphoria indicator)
  - DeFi TVL declining + Fear index above 75 (extreme greed) + technical resistance hit

## Examples of Specific Actionable Recommendations for Experts:
  Short-term Trading (1-7 days):

  - "BTC showing whale accumulation at $42K support, RSI oversold, Reddit sentiment turning positive - Consider 3-5% position"
  - "ETH exchange inflows spiking, DeFi TVL dropping 15%, social sentiment extremely bullish - Reduce exposure by 20%"

  Medium-term Positioning (1-4 weeks):

  - "Institutional adoption news + consistent whale buying + DeFi innovation surge - Increase BTC allocation to 60%"
  - "Regulatory uncertainty + declining network activity + social sentiment shift - Move to stablecoins, wait for clarity"

  Risk Management:

  - "Correlation analysis shows BTC/ETH moving together - Diversify beyond crypto or use hedging strategies"
  - "Whale wallet flagged unusual activity - Set tighter stop losses for next 48 hours"

  Market Timing:

  - "Fear index at 15 + major whale buy + positive DeFi developments = High probability bottom forming"
  - "All sentiment indicators bullish + whales selling + exchange inflows = Top signal, prepare for correction"


### Retail-Friendly Actionable Insights

  Simple Buy/Hold/Sell Decisions:

  - "BTC showing strong fundamentals + whale buying activity. Recommend: Add $50-100 to your monthly BTC allocation"
  - "ETH network growth + positive DeFi trends. Recommend: Consider 60% BTC, 40% ETH split in your portfolio"
  - "Market showing extreme fear but fundamentals strong. Recommend: This could be a good buying opportunity for long-term holders"

  Portfolio Allocation Guidance:

  - "High correlation between BTC/ETH detected. Consider: Adding some stablecoin allocation (10-20%) for balance"
  - "DeFi sector outperforming. Consider: Slightly increase ETH allocation from 30% to 40%"

  Timing Recommendations:
  - "Multiple positive signals aligning. Recommend: Good time for your weekly $100 crypto purchase"
  - "Warning signals detected. Recommend: Skip this week's purchase, wait for better entry point"
  - "Major whales selling + negative news. Recommend: Consider taking some profits if you're up significantly"

  Risk Warnings for Retail:
  - "Social media showing extreme excitement + whales selling. Warning: Avoid FOMO buying, price may correct soon"
  - "Market sentiment very negative but fundamentals unchanged. Opportunity: Good time for dollar-cost averaging"

  Platform-Specific Actions:
  - "Set buy order on Pluang for next dip below $41K BTC"
  - "Consider reducing auto-invest amount for next 2 weeks"
  - "Good time to use Pluang's recurring buy feature"

## Implementation 

### Best practices 
- First create a plan and overall project structure. 
- Each file should be testable and modular, with a main function. 
- Focus each todo on implementing 1 testable feature. I'd like to test things before moving on. 
- No version pinning before install - Let conda/pip resolve compatible versions
- Incremental approach - Add dependencies as we build tools
- Export strategy - conda env export > environment-lock.yml after testing

Workflow for environment :
conda is in `~/miniconda3/bin/conda`

Environment Commands:
- Create env: `~/miniconda3/bin/conda env create -f environment.yml`
- Activate: `source ~/miniconda3/bin/activate crypto-agent`
- Test tools: `python src/tools/serper_tool.py`
- Export lock: `conda env export > environment-lock.yml`

  1. Add code → Update pyproject.toml and readme.md → Test → Export lock file
  2. This way we get actual working versions instead of guessing

  ### Implementation plan day 1
  
  We'll start with the analyst agents on day 1. 
    Implementation Structure:

  - LangChain LLM (OpenAI/Claude) with tool binding
  - One agent per analysis type - standalone, focused implementation
  - Custom tools for each agent - API clients as LangChain tools
  - Prompt engineering focus - Clear analysis instructions per agent

  Day 1 Agents:

  1. Technical Analysis Agent + CoinGecko tool
  2. On-Chain Analysis Agent + Blockchair/Etherscan tools
  3. DeFi Fundamentals Agent + DeFiLlama tool
  4. Sentiment Fusion Agent + Serper/Reddit/Fear&Greed tools

Each agent will be a simple react agent with its respective tools and checkpointer memory. You can use Langchain example here - https://python.langchain.com/docs/tutorials/agents/ 


  Testing Approach:

  - Individual API testing with some test cases
  - Individual agent testing - Each agent runs independently on BTC/ETH
  - Prompt validation - Verify analysis quality and reasoning chains
  - Agent inputs and outputs - Finalize inputs and outputs for each agent
  - Tool integration - Ensure API data flows correctly to LLM
  - LangSmith traces - Monitor tool calls and agent decisions

