"""
Low-level AI API client.

Responsible ONLY for talking to an OpenAI-compatible chat-completions API.
It never contains any aptitude/DI logic -- that all lives in the core
modules. If no API key is configured, or the call fails for any reason
(no internet, timeout, invalid response, ...), this raises AIUnavailableError
so the higher-level ai_service can show a graceful fallback message instead
of crashing the application.
"""

from __future__ import annotations

from src.config.settings import AISettings, get_ai_settings


class AIUnavailableError(Exception):
    """Raised whenever the AI Assistant cannot currently be used."""


class AIClient:
    """Thin wrapper around an OpenAI-compatible client.

    The real `openai` SDK is imported lazily inside __init__ so that the
    rest of the application (and its tests) never fail to import even if
    the package is missing or misconfigured.
    """

    def __init__(self, settings: AISettings | None = None) -> None:
        self.settings = settings or get_ai_settings()
        self._client = None

        if self.settings.is_configured:
            try:
                from openai import OpenAI  # imported lazily
                self._client = OpenAI(
                    api_key=self.settings.api_key,
                    base_url=self.settings.base_url,
                )
            except Exception:
                # If the SDK itself cannot be constructed, treat AI as
                # unavailable rather than crashing the whole application.
                self._client = None

    @property
    def is_available(self) -> bool:
        return self._client is not None

    def chat(self, system_prompt: str, user_prompt: str,
              max_tokens: int = 500, temperature: float = 0.4) -> str:
        """Send a single-turn chat request and return the assistant's text.

        Raises:
            AIUnavailableError: if the client is not configured, or the
                request fails for any reason (network, timeout, API error,
                malformed response, ...).
        """
        if not self.is_available:
            raise AIUnavailableError(
                "AI Assistant is currently unavailable. "
                "Core solving features are still fully functional."
            )
        try:
            response = self._client.chat.completions.create(
                model=self.settings.model,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=20,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            content = response.choices[0].message.content
            if not content or not content.strip():
                raise AIUnavailableError("The AI returned an empty response.")
            return content.strip()
        except AIUnavailableError:
            raise
        except Exception as exc:  # noqa: BLE001 - any SDK/network error becomes AIUnavailableError
            raise AIUnavailableError(
                f"AI explanation is currently unavailable ({exc.__class__.__name__})."
            ) from exc
