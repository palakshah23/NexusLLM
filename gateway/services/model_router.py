
import os
from typing import Optional


class ModelRouter:
    POLICIES = ("cheap", "balanced", "quality")

    ENV_KEYS = {
        "cheap": "NEXUSLLM_MODEL_CHEAP",
        "balanced": "NEXUSLLM_MODEL_BALANCED",
        "quality": "NEXUSLLM_MODEL_QUALITY",
    }

    @classmethod
    def select(
        cls,
        policy: str = "balanced",
        estimated_input_tokens: Optional[int] = None,
        estimated_output_tokens: Optional[int] = None,
    ) -> str:
        policy = policy.lower().strip()

        if policy not in cls.POLICIES:
            raise ValueError(f"Unsupported routing policy: {policy}")

        model = os.getenv(cls.ENV_KEYS[policy])

        if not model:
            raise ValueError(
                f"No model configured for '{policy}'. "
                f"Set {cls.ENV_KEYS[policy]} in .env."
            )

        # Validate token estimates when supplied.
        for name, value in (
            ("estimated_input_tokens", estimated_input_tokens),
            ("estimated_output_tokens", estimated_output_tokens),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{name} cannot be negative.")

        return model
