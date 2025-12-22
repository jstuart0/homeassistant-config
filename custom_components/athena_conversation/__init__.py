"""The Athena Conversation Agent integration."""
from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "athena_conversation"
PLATFORMS: list[Platform] = [Platform.CONVERSATION]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Athena Conversation Agent integration."""
    # Set up the conversation platform
    await hass.helpers.discovery.async_load_platform(
        Platform.CONVERSATION, DOMAIN, {}, config
    )
    return True
