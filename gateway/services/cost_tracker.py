
from datetime import datetime, timezone

from gateway.services.model_pricing import ModelPricing


class CostTracker:
    """Tracks token usage and estimated model costs."""

    records = []

    @classmethod
    def record(
        cls,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> dict:

        cost = ModelPricing.calculate_cost(
            model,
            input_tokens,
            output_tokens,
        )

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost_usd": round(cost, 10),
        }

        cls.records.append(record)

        return record

    @classmethod
    def get_summary(cls) -> dict:
        return {
            "total_requests": len(cls.records),
            "total_input_tokens": sum(
                r["input_tokens"] for r in cls.records
            ),
            "total_output_tokens": sum(
                r["output_tokens"] for r in cls.records
            ),
            "total_estimated_cost_usd": round(
                sum(r["estimated_cost_usd"] for r in cls.records),
                10,
            ),
        }
