import os
import logging
from openai import AsyncOpenAI
from src.schema import SentimentAnalysis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("SentinelAgent")

class SentinelAgent:
    """
    Core agent responsible for analyzing geopolitical transcripts and executing trades.
    """

    def __init__(self):
        """Initializes the agent and strict confidence thresholds."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.critical("OPENAI_API_KEY environment variable is missing.")
            raise ValueError("OPENAI_API_KEY is missing.")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.confidence_threshold = 0.75

    async def analyze_transcript(self, transcript_chunk: str) -> SentimentAnalysis:
        """
        Analyzes a chunk of transcript using GPT-4o's Structured Outputs.
        """
        system_prompt = (
            "You are a highly accurate quantitative geopolitical analyst. "
            "Analyze the given transcript from a political press conference. "
            "Determine if the rhetoric will drive XAU/USD (Gold) and WTI Crude prices UP (BULLISH) or DOWN (BEARISH). "
            "Look for keywords regarding sanctions, military action, or supply chain disruptions. "
            "If the rhetoric is ambiguous or unrelated to markets, return NEUTRAL."
        )

        logger.info("Sending transcript chunk to LLM for deterministic sentiment analysis.")
        
        try:
            response = await self.client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript_chunk}
                ],
                response_format=SentimentAnalysis,
                temperature=0.0, # Zero temperature for maximum determinism
            )
            
            parsed_result = response.choices[0].message.parsed
            if parsed_result is None:
                 raise ValueError("LLM returned an empty or invalid parsed response.")
            
            logger.info("Successfully parsed LLM sentiment analysis.")
            return parsed_result

        except Exception as e:
            logger.error(f"Analysis failed due to error: {e}")
            return SentimentAnalysis(
                market_direction="NEUTRAL",
                reasoning=f"Error encountered during analysis: {str(e)}",
                confidence_score=0.0
            )

    async def execute_trade(self, analysis: SentimentAnalysis) -> bool:
        """
        Evaluates the analysis and routes the trade if kill-switch conditions are cleared.
        """
        logger.info(f"Agent Reasoning: {analysis.reasoning}")

        if analysis.market_direction == "NEUTRAL":
            logger.info("Signal is NEUTRAL. Holding position. No trade executed.")
            return False

        if analysis.confidence_score < self.confidence_threshold:
            logger.warning(
                f"KILL-SWITCH ENGAGED: Confidence ({analysis.confidence_score}) "
                f"is below the strict threshold of {self.confidence_threshold}. Trade aborted."
            )
            return False

        action = "BUY Long" if analysis.market_direction == "BULLISH" else "SELL Short"
        
        logger.info("=" * 60)
        logger.info(f"🚀 EXECUTING TRADE: {action} on XAU/USD and WTI")
        logger.info(f"🎯 Confidence Metric: {analysis.confidence_score}")
        logger.info("=" * 60)
        
        # NOTE: MetaTrader5 package is Windows-only. Abstracting to prevent Linux Docker crashes.
        # In a Windows production environment, replace this with mt5.order_send(...)
        logger.info("Broker API (Simulated) successfully received execution command.")
        
        return True