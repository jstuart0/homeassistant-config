"""Athena Conversation Agent for Home Assistant."""
from __future__ import annotations

import asyncio
import aiohttp
import logging
from typing import Any, Literal

from homeassistant.components.conversation import ConversationEntity, ConversationResult
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

ORCHESTRATOR_URL = "http://192.168.10.167:8001/query"


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict[str, Any],
    async_add_entities: AddEntitiesCallback,
    discovery_info: dict[str, Any] | None = None,
) -> None:
    """Set up the Athena conversation agent."""
    _LOGGER.info("Setting up Athena conversation agent")
    async_add_entities([AthenaConversationAgent(hass)], True)


class AthenaConversationAgent(ConversationEntity):
    """Athena conversation agent."""

    _attr_name = "Athena Assistant"
    _attr_unique_id = "athena_conversation_agent"

    def __init__(self, hass: HomeAssistant):
        """Initialize the Athena conversation agent."""
        self.hass = hass
        _LOGGER.info("Initializing Athena conversation agent with orchestrator at %s", ORCHESTRATOR_URL)

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return ["en"]

    async def async_process(
        self, user_input: str, conversation_id: str | None, context: dict[str, Any]
    ) -> ConversationResult:
        """Process a sentence."""
        _LOGGER.info("Processing user input: %s", user_input)

        try:
            # Call orchestrator
            async with aiohttp.ClientSession() as session:
                payload = {
                    "query": user_input,
                    "session_id": conversation_id or "ha-default"
                }

                _LOGGER.debug("Sending request to orchestrator: %s", payload)

                async with session.post(
                    ORCHESTRATOR_URL,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        _LOGGER.error("Orchestrator returned status %s: %s", response.status, error_text)
                        return ConversationResult(
                            response_type="error",
                            response="I'm having trouble connecting to my AI brain right now. Please try again.",
                        )

                    result = await response.json()
                    _LOGGER.debug("Received response from orchestrator: %s", result)

                    # Extract the response text
                    response_text = result.get("answer", "I'm not sure how to respond to that.")
                    intent = result.get("intent", "unknown")
                    confidence = result.get("confidence", 0.0)

                    _LOGGER.info("Orchestrator response (intent=%s, confidence=%.2f): %s", 
                               intent, confidence, response_text[:100])

                    return ConversationResult(
                        response_type="query_answer",
                        response=response_text,
                    )

        except asyncio.TimeoutError:
            _LOGGER.error("Timeout calling orchestrator")
            return ConversationResult(
                response_type="error",
                response="Sorry, that took too long. Please try asking again.",
            )

        except aiohttp.ClientError as err:
            _LOGGER.error("Network error calling orchestrator: %s", err)
            return ConversationResult(
                response_type="error",
                response="I'm having trouble connecting to my AI brain. Please check the network.",
            )

        except Exception as err:
            _LOGGER.error("Unexpected error processing conversation: %s", err, exc_info=True)
            return ConversationResult(
                response_type="error",
                response="I'm sorry, something unexpected happened. Please try again.",
            )
