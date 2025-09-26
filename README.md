# Crypto Investment Analyst

Multi-Agent AI system that analyzes cryptocurrency data and generates investment reports with actionable recommendations.

## Setup Instructions (Mac M1/M2)

### 1. Create Conda Environment
```bash
# Create environment with M1-optimized packages
conda env create -f environment.yml

# Activate environment
conda activate crypto-agent
```

### 2. Environment Variables
The file .env.example includes all the API keys that need to be provided for the code to run. 

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```


### 3. Test Serper Tool
```bash
# Test the Serper integration
python src/tools/serper_tool.py
```

## Development Workflow

### Adding New Dependencies
As we add more tools, update dependencies:

```bash
# Add to pyproject.toml dependencies, then:
pip install -e .

# Export final environment
conda env export > environment-lock.yml
```

## Agent Architecture

The system uses a multi-agent architecture with a supervisor coordinating specialized analysis agents:

### System Flow Diagram
```
                                   USER
                                    |
                         [Investment Question]
                                    |
                                    v
                          ┌─────────────────┐
                          │   SUPERVISOR    │
                          │  (Lead Crypto   │
                          │   Analyst)      │
                          └─────────────────┘
                                    |
                    ┌───────────────┼───────────────┐
                    |               |               |
                    |               |               |
                    v               v               v
           ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
           │ TECHNICAL    │ │ WEB SENTIMENT│ │  CHALLENGER  │
           │ ANALYSIS     │ │   AGENT      │ │   AGENT      │
           │   AGENT      │ │              │ │              │
           └──────────────┘ └──────────────┘ └──────────────┘
                    |               |               |
            [get_multiple_     [serper_search]     [No tools -
             indicators]       [fear_greed_index]   validation only]
                    |               |               |
                    v               v               |
           ┌──────────────┐ ┌──────────────┐       |
           │  TaaPI API   │ │ Serper API   │       |
           │ (Technical   │ │ (News/Web),  │       |
           │ Indicators)  │ │              │       |
           └──────────────┘ └──────────────┘       |
                    |               |               |
                    └───────────────┼───────────────┘
                                    |
                            [Analysis Results]
                                    |
                                    v
                          ┌─────────────────┐
                          │   SUPERVISOR    │
                          │ [Validation &   │
                          │  Synthesis]     │
                          └─────────────────┘
                                    |
                            [Final Report with
                             Buy/Sell/Hold
                             Recommendations]
                                    |
                                    v
                                   USER

Workflow Pattern:
1. User → Supervisor (question + investor profile)
2. Supervisor → Technical Agent → TaaPI API
3. Supervisor → Sentiment Agent → Serper API + Fear/Greed Index
4. Supervisor → Challenger Agent (validate findings)
5. Supervisor → [Re-analyze if needed based on challenger feedback]
6. Supervisor → User (final investment recommendation)
```

### Supervisor Agent (`src/agents/supervisor_agent.py`)
**Lead Crypto Analyst** - Orchestrates the analysis workflow and provides final investment recommendations for BTC and ETH.

**Workflow:**

User-profile is set in user_profiles.json - this is a proxy for current user-holdings and investment style. 

1. The supervisor agent takes user-profile and question. It Calls sentiment and technical analysis agents to gather initial data
2. Uses challenger agent to validate findings and identify gaps
3. Re-analyzes based on challenger feedback if needed
4. Provides final buy/sell/hold recommendation with confidence levels
5. For multi-turn conversations, user can ask follow-up questions. 



### Specialized Agents
- **Technical Analysis Agent** - Analyzes price data, technical indicators, volume patterns using TaaPI API
- **Web Sentiment Agent** - Analyzes market sentiment from news, social media, and whale activity using Serper API
- **Challenger Agent** - Cross-validates findings, flags inconsistencies, ensures thorough evaluation

### Multi-Agent Coordination
- **LangGraph Supervisor** - Routes tasks between agents based on analysis needs
- **Memory Checkpointing** - Maintains conversation state across multi-turn interactions
- **Tool Handoffs** - Seamless delegation between specialized agents

## Project Structure
```
src/
├── agents/         # Multi-agent system
│   ├── supervisor_agent.py      # Main coordinator
│   ├── technical_analysis_agent.py
│   ├── web_sentiment_agent.py
│   └── challenger_agent.py
├── tools/          # API integrations
│   ├── serper_tool.py           # News/web search
│   └── taapi_tool.py            # Technical indicators
└── utils/          # Reporting utilities

reports/            # Sample analysis outputs
tests/              # Test suite
```

## Testing & Usage

### Run Analysis Demos
```bash
# Generate investment reports for different investor types
python main.py
```

This will generate:
- Single-turn analysis reports for different investor profiles
- Multi-turn conversation demonstrating human-in-the-loop interaction
- Sample outputs saved to `reports/` directory

### Test Individual Tools
```bash
# Test Serper integration
python src/tools/serper_tool.py

# Test TaaPI integration
python src/tools/taapi_tool.py
```

### Sample Outputs
Check `reports/` directory for example analysis reports:
- `report_aggressive_young.md` - High-risk investor analysis
- `report_conservative_beginner.md` - Conservative strategy
- `report_recovery_investor.md` - Post-loss recovery approach
- `multi_turn_demo.md` - Multi-turn conversation example
