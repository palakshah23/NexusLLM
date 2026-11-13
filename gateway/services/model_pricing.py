
class ModelPricing:
    """
    Model pricing registry.
    Prices are USD per 1 million tokens.
    """

    PRICING = {
        "groq-cheap": {
            "provider_model": "openai/gpt-oss-20b",
            "input_per_million": 0.075,
            "output_per_million": 0.30,
        },
        "groq-llama": {
            "provider_model": "openai/gpt-oss-120b",
            "input_per_million": 0.15,
            "output_per_million": 0.60,
        },
        "groq-quality": {
            "provider_model": "qwen/qwen3.8-27b",
            "input_per_million": 0.80,
            "output_per_million": 4.00,
        },
    }

    @classmethod
    def get_pricing(cls, model: str) -> dict:
        if model not in cls.PRICING:
            raise ValueError(f"Pricing not configured for model: {model}")

        return cls.PRICING[model]

    @classmethod
    def calculate_cost(
        cls,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        pricing = cls.get_pricing(model)

        return (
            input_tokens * pricing["input_per_million"]
            + output_tokens * pricing["output_per_million"]
        ) / 1_000_000
