import pytest
import os
from unittest.mock import AsyncMock, patch
from src.schema import SentimentAnalysis
from src.agent import SentinelAgent

os.environ["OPENAI_API_KEY"] = "sk-test-key"

@pytest.fixture
def mock_agent():
    return SentinelAgent()

@pytest.mark.asyncio
async def test_analyze_transcript_success(mock_agent):
    """Verifies structured parsing of a bullish geopolitical threat."""
    mock_response = SentimentAnalysis(
        market_direction="BULLISH",
        reasoning="Mention of naval blockades restricts supply, driving safe-haven assets up.",
        confidence_score=0.95
    )

    with patch.object(mock_agent.client.beta.chat.completions, 'parse', new_callable=AsyncMock) as mock_parse:
        mock_parse.return_value.choices = [
            type('obj', (object,), {'message': type('obj', (object,), {'parsed': mock_response})()})()
        ]

        result = await mock_agent.analyze_transcript("We are initiating a blockade.")
        
        assert result.market_direction == "BULLISH"
        assert result.confidence_score == 0.95
        mock_parse.assert_called_once()

@pytest.mark.asyncio
async def test_execute_trade_kill_switch(mock_agent):
    """Verifies trade abortion when confidence is below the 0.75 threshold."""
    analysis = SentimentAnalysis(
        market_direction="BULLISH",
        reasoning="Slightly aggressive tone, but unconfirmed.",
        confidence_score=0.60  
    )

    trade_executed = await mock_agent.execute_trade(analysis)
    assert trade_executed is False

@pytest.mark.asyncio
async def test_execute_trade_success(mock_agent):
    """Verifies execution routing when confidence is high."""
    analysis = SentimentAnalysis(
        market_direction="BULLISH",
        reasoning="Explicit threat of supply restriction.",
        confidence_score=0.90
    )

    trade_executed = await mock_agent.execute_trade(analysis)
    assert trade_executed is True