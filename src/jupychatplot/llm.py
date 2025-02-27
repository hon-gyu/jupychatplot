import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()


def get_llm(
    model_name: Literal[
        "google/gemini-2.0-flash-001", "openai/gpt-4o"
    ] = "google/gemini-2.0-flash-001",
) -> Model:
    return OpenAIModel(
        model_name,
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    )
