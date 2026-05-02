# fin_agent is a high-frequency, NLP-driven quantitative trading agent. It listens to live political press conferences, performs sub-second semantic sentiment analysis, and executes directional trades (BULLISH/BEARISH) on commodities like WTI Crude and safe-haven assets like XAU/USD (Gold) before the broader market can parse the rhetoric.

Quick Start (Cursor Ready)
1. Environment Setup:
    Ensure you have `.env` configured with your `OPENAI_API_KEY`.
2. Run Simulation:
   bash
   pip install -r requirements.txt
   python -m src.main
3. Run Mock Test Suite
   pytest tests/
