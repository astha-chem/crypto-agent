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
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required API keys:
- `SERPER_API_KEY` - Get from [serper.dev](https://serper.dev)
- `OPENAI_API_KEY` - Get from [OpenAI](https://platform.openai.com/api-keys)
- `LANGCHAIN_API_KEY` - Get from [LangSmith](https://smith.langchain.com/) (optional, for tracing)

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

### Current Tools
- ✅ Serper API (news & web search)
- 🚧 CoinGecko API (coming next)
- 🚧 Etherscan API
- 🚧 Other APIs...

## Project Structure
```
src/
├── tools/          # API integrations
├── agents/         # Analysis agents
├── core/           # Core system
├── models/         # Data models
└── utils/          # Utilities

tests/              # Test suite
config/             # Configuration
```

## Testing
```bash
pytest tests/
```
