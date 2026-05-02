"""
测试用例 - 代码审查 Agent
"""

import pytest
from src.agents.code_review_agent import CodeReviewAgent


@pytest.fixture
def code_review_agent():
    return CodeReviewAgent()


@pytest.mark.asyncio
async def test_analyze_simple_code(code_review_agent):
    """测试简单代码分析"""
    code = """
    def hello():
        print("Hello World")
    """
    result = await code_review_agent.analyze(code, language="python")
    assert result["agent"] == "CodeReviewAgent"
    assert result["language"] == "python"
    assert "issues" in result


@pytest.mark.asyncio
async def test_analyze_code_with_bug(code_review_agent):
    """测试有 Bug 的代码"""
    code = """
    def divide(a, b):
        return a / b
    """
    result = await code_review_agent.analyze(code, language="python")
    assert result is not None
    assert "issues" in result


@pytest.mark.asyncio
async def test_batch_analyze(code_review_agent):
    """测试批量分析"""
    files = [
        {"path": "test1.py", "content": "def foo(): pass", "language": "python"},
        {"path": "test2.py", "content": "def bar(): pass", "language": "python"},
    ]
    results = await code_review_agent.batch_analyze(files)
    assert len(results) == 2
