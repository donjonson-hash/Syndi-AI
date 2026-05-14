import pytest
import asyncio
from agents import get_kristina

@pytest.mark.asyncio
async def test_kristina():
    """Тест Кристины"""
    agent = get_kristina()
    response = await agent.process("Hello")
    assert response is not None
    assert response.text is not None
    assert len(response.text) > 0
