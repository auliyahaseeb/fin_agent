from pydantic import BaseModel, Field
from typing import Literal

class SentimentAnalysis(BaseModel):
    """
    Pydantic schema enforcing the exact structure the LLM must return.
    """
    market_direction: Literal["BULLISH", "BEARISH", "NEUTRAL"] = Field(
        description="Predicted direction for safe-haven assets (Gold/XAU) and Energy based on rhetoric."
    )
    reasoning: str = Field(
        description="Step-by-step logical deduction of the speech content and its geopolitical implications."
    )
    confidence_score: float = Field(
        ge=0.0, 
        le=1.0, 
        description="Mathematical confidence in the prediction, ranging from 0.0 to 1.0."
    )