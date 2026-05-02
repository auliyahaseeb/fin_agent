import asyncio
import logging
import os
from src.agent import SentinelAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SentinelSimulation")

async def run_simulation():
    """Runs a mock live feed simulation for the Loom video demonstration."""
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "sk-mock-key-for-initialization"

    try:
        agent = SentinelAgent()
    except ValueError as e:
        logger.error(f"Initialization Error: {e}")
        return

    mock_transcript = (
        "We are closely monitoring the maritime bottlenecks in the Middle East. "
        "The recent hostile actions are unacceptable. Effective immediately, "
        "we are imposing strict naval blockades on the primary export routes. "
        "We will not hesitate to use military assets to enforce this."
    )
    
    logger.info("--- STARTING LIVE DATA INGESTION ---")
    logger.info(f"Incoming Stream Transcribed: '{mock_transcript}'")
    
    analysis_result = await agent.analyze_transcript(mock_transcript)
    await agent.execute_trade(analysis_result)
    
    logger.info("--- SIMULATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_simulation())