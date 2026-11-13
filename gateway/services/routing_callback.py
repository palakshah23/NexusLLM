
from litellm.integrations.custom_logger import CustomLogger
from litellm.proxy.proxy_server import DualCache, UserAPIKeyAuth
from litellm.types.utils import CallTypesLiteral

from gateway.services.model_router import ModelRouter


class NexusRoutingCallback(CustomLogger):
    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: CallTypesLiteral,
    ):
        metadata = data.get("metadata") or {}

        nexus_metadata = metadata.get("nexusllm") or {}

        policy = (
            data.pop("routing_policy", None)
            or metadata.get("routing_policy")
            or nexus_metadata.get("routing_policy")
            or "balanced"
        )

        messages = data.get("messages") or []

        estimated_input_tokens = data.get("max_input_tokens")
        estimated_output_tokens = data.get("max_tokens")

        selected_model = ModelRouter.select(
            policy,
            estimated_input_tokens=estimated_input_tokens,
            estimated_output_tokens=estimated_output_tokens,
        )

        data["model"] = selected_model

        metadata["nexusllm_routing"] = {
            "policy": policy,
            "selected_model": selected_model,
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_output_tokens": estimated_output_tokens,
        }

        data["metadata"] = metadata

        return data


proxy_handler_instance = NexusRoutingCallback()
