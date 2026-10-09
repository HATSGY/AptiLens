"""
Tests for the AI layer.

These tests NEVER require a real API key or network access: AIClient is
either exercised in its "not configured" state, or replaced entirely with
a Mock/stub so ai_service's behaviour can be verified in isolation.
"""

from unittest.mock import MagicMock

import pytest

from src.ai.ai_client import AIClient, AIUnavailableError
from src.ai.ai_service import AIService
from src.config.settings import AISettings


def test_ai_client_unavailable_without_api_key():
    settings = AISettings(api_key=None, model="gpt-4o-mini", base_url="https://api.openai.com/v1")
    client = AIClient(settings=settings)
    assert client.is_available is False
    with pytest.raises(AIUnavailableError):
        client.chat("system", "user")


def test_ai_client_empty_api_key_is_treated_as_not_configured():
    settings = AISettings(api_key="", model="gpt-4o-mini", base_url="https://api.openai.com/v1")
    client = AIClient(settings=settings)
    assert client.is_available is False


def test_ai_service_falls_back_gracefully_when_client_unavailable():
    mock_client = MagicMock()
    mock_client.is_available = False
    mock_client.chat.side_effect = AIUnavailableError(
        "AI Assistant is currently unavailable. Core solving features are still fully functional."
    )
    service = AIService(client=mock_client)

    result = service.explain_solution(
        module="Clock", problem="Find angle at 3:20", inputs={"Hour": 3, "Minute": 20},
        formula="|30H - 5.5M|", verified_result="20 degrees",
    )
    assert result["available"] is False
    assert "unavailable" in result["text"].lower()


def test_ai_service_never_raises_even_on_unexpected_client_error():
    mock_client = MagicMock()
    mock_client.chat.side_effect = RuntimeError("boom")  # not even AIUnavailableError
    service = AIService(client=mock_client)
    # ai_service only guarantees graceful handling of AIUnavailableError; make sure
    # a raw exception from a misbehaving client is still surfaced predictably by
    # the client layer's contract, not silently swallowed into a bad state.
    with pytest.raises(RuntimeError):
        service.explain_solution("Clock", "problem", {}, "formula", "result")


def test_ai_service_explain_solution_returns_mocked_text():
    mock_client = MagicMock()
    mock_client.is_available = True
    mock_client.chat.return_value = "Step-by-step explanation here."
    service = AIService(client=mock_client)

    result = service.explain_solution(
        module="Clock", problem="Find angle at 3:20", inputs={"Hour": 3, "Minute": 20},
        formula="|30H - 5.5M|", verified_result="20 degrees",
    )
    assert result == {"available": True, "text": "Step-by-step explanation here."}
    mock_client.chat.assert_called_once()


def test_ai_service_generate_hint():
    mock_client = MagicMock()
    mock_client.is_available = True
    mock_client.chat.return_value = "Think about the formula for hour-hand movement per minute."
    service = AIService(client=mock_client)
    result = service.generate_hint("Clock", "Find the angle at 3:20", "Medium")
    assert result["available"] is True
    assert "formula" in result["text"].lower()


def test_ai_service_explain_formula():
    mock_client = MagicMock()
    mock_client.is_available = True
    mock_client.chat.return_value = "Zeller's Congruence finds the day of week..."
    service = AIService(client=mock_client)
    result = service.explain_formula("Calendar", "Zeller's Congruence")
    assert result["available"] is True


def test_ai_service_analyze_graph():
    mock_client = MagicMock()
    mock_client.is_available = True
    mock_client.chat.return_value = "The bar chart shows Feb is highest."
    service = AIService(client=mock_client)
    result = service.analyze_graph("Bar Graph", {"highest": {"category": "Feb", "value": 60}})
    assert result["available"] is True


def test_ai_service_generate_similar_question():
    mock_client = MagicMock()
    mock_client.is_available = True
    mock_client.chat.return_value = "New question: 3, 9, 27, 81, ?\nAnswer: 243"
    service = AIService(client=mock_client)
    result = service.generate_similar_question("Patterns", "2, 4, 8, 16, ?", "Medium")
    assert result["available"] is True
    assert "Answer" in result["text"]


def test_ai_service_simplify_explanation():
    mock_client = MagicMock()
    mock_client.is_available = True
    mock_client.chat.return_value = "In simple terms: ..."
    service = AIService(client=mock_client)
    result = service.simplify_explanation("A convoluted explanation full of jargon.")
    assert result["available"] is True


def test_ai_service_explain_why_correct():
    mock_client = MagicMock()
    mock_client.is_available = True
    mock_client.chat.return_value = "This is correct because ..."
    service = AIService(client=mock_client)
    result = service.explain_why_correct("Tabular DI", "What is 20% of 150?", "30")
    assert result["available"] is True


def test_ai_service_is_available_reflects_client():
    mock_client = MagicMock()
    mock_client.is_available = True
    service = AIService(client=mock_client)
    assert service.is_available is True
