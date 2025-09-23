  Directory structure
  crypto-agent/
  ├── src/
  │   ├── agents/
  │   │   ├── __init__.py
  │   │   ├── base_agent.py                    # Base agent class with common functionality
  │   │   ├── technical_analysis_agent.py      # Agent #5: Technical Analysis
  │   │   ├── onchain_analysis_agent.py        # Agent #6: On-Chain Analysis  
  │   │   ├── defi_fundamentals_agent.py       # Agent #7: DeFi Fundamentals
  │   │   ├── sentiment_fusion_agent.py        # Agent #8: Sentiment Fusion
  │   │   ├── intelligence_fusion_agent.py     # Agent #2: Intelligence Fusion
  │   │   ├── action_recommender_agent.py      # Agent #3: Action Recommender
  │   │   ├── analysis_challenger_agent.py     # Agent #4: Analysis Challenger
  │   │   └── user_interface_agent.py          # Agent #1: User Interface
  │   │
  │   ├── tools/
  │   │   ├── __init__.py
  │   │   ├── base_tool.py                     # Base tool class
  │   │   ├── coingecko_tool.py               # CoinGecko API integration
  │   │   ├── blockchair_tool.py              # Blockchair API (Bitcoin on-chain)
  │   │   ├── etherscan_tool.py               # Etherscan API (Ethereum on-chain)
  │   │   ├── defillama_tool.py               # DeFiLlama API integration
  │   │   ├── serper_tool.py                  # Serper API (search/news)
  │   │   ├── reddit_tool.py                  # Reddit API integration
  │   │   └── fear_greed_tool.py              # Fear & Greed Index API
  │   │
  │   ├── core/
  │   │   ├── __init__.py
  │   │   ├── orchestrator.py                 # Main system orchestrator
  │   │   ├── user_profile.py                 # User profile management
  │   │   ├── config.py                       # Configuration management
  │   │   └── exceptions.py                   # Custom exceptions
  │   │
  │   ├── models/
  │   │   ├── __init__.py
  │   │   ├── analysis_models.py              # Data models for analysis results
  │   │   ├── recommendation_models.py        # Data models for recommendations
  │   │   └── user_models.py                  # User profile data models
  │   │
  │   └── utils/
  │       ├── __init__.py
  │       ├── logging.py                      # Logging configuration
  │       ├── validation.py                   # Data validation utilities
  │       └── formatting.py                  # Output formatting utilities
  │
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py                         # Pytest configuration and fixtures
  │   │
  │   ├── test_agents/
  │   │   ├── __init__.py
  │   │   ├── test_technical_analysis_agent.py
  │   │   ├── test_onchain_analysis_agent.py
  │   │   ├── test_defi_fundamentals_agent.py
  │   │   ├── test_sentiment_fusion_agent.py
  │   │   ├── test_intelligence_fusion_agent.py
  │   │   ├── test_action_recommender_agent.py
  │   │   ├── test_analysis_challenger_agent.py
  │   │   └── test_user_interface_agent.py
  │   │
  │   ├── test_tools/
  │   │   ├── __init__.py
  │   │   ├── test_coingecko_tool.py
  │   │   ├── test_blockchair_tool.py
  │   │   ├── test_etherscan_tool.py
  │   │   ├── test_defillama_tool.py
  │   │   ├── test_serper_tool.py
  │   │   ├── test_reddit_tool.py
  │   │   └── test_fear_greed_tool.py
  │   │
  │   ├── test_core/
  │   │   ├── __init__.py
  │   │   ├── test_orchestrator.py
  │   │   ├── test_user_profile.py
  │   │   └── test_config.py
  │   │
  │   ├── fixtures/
  │   │   ├── __init__.py
  │   │   ├── sample_data.py                  # Sample API responses for testing
  │   │   └── user_profiles.py                # Test user profiles
  │   │
  │   └── integration/
  │       ├── __init__.py
  │       ├── test_agent_integration.py       # Cross-agent integration tests
  │       └── test_full_workflow.py           # End-to-end workflow tests
  │
  ├── config/
  │   ├── default.yaml                        # Default configuration
  │   ├── development.yaml                    # Development environment config
  │   └── production.yaml                     # Production environment config
  │
  ├── data/
  │   ├── user_profiles.json                  # Example user profiles for testing
  │   └── historical/                         # Historical data for backtesting
  │       ├── btc_ohlc.json
  │       ├── eth_ohlc.json
  │       └── whale_events.json
  │
  ├── scripts/
  │   ├── run_agent.py                        # Script to run individual agents
  │   ├── run_analysis.py                     # Script to run full analysis
  │   └── backtest.py                         # Backtesting script
  │
  ├── requirements.txt                        # Python dependencies
  ├── pyproject.toml                          # Project configuration
  ├── README.md                               # Project documentation
  └── .env.example                            # Environment variables template