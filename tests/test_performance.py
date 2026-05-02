"""
测试用例 - 性能优化 Agent
"""

import pytest
from src.agents.performance_agent import PerformanceAgent


@pytest.fixture
def performance_agent():
    return PerformanceAgent()


@pytest.mark.asyncio
async def test_analyze_loop_performance(performance_agent):
    """测试循环性能分析"""
    code = """
    def find_duplicates(items):
        duplicates = []
        for i in range(len(items)):
            for j in range(len(items)):
                if items[i] == items[j] and i != j:
                    duplicates.append(items[i])
        return duplicates
    """
    result = await performance_agent.analyze(code, language="python")
    assert result["agent"] == "PerformanceAgent"
    assert result["language"] == "python"


@pytest.mark.asyncio
async def test_general_tips(performance_agent):
    """测试通用优化建议"""
    tips = performance_agent.PERFORMANCE_TIPS.get("python", [])
    assert len(tips) > 0


@pytest.mark.asyncio
async def test_suggest_alternatives(performance_agent):
    """测试替代方案生成"""
    code = """
    result = []
    for i in range(1000):
        result.append(i * 2)
    """
    # 注意：这个测试需要 API key
    # suggestion = await performance_agent.suggest_alternatives(code)
    # assert suggestion is not None
