"""
集成测试 - 完整分析流程
"""

import pytest
from src.services.code_analyzer import CodeAnalyzer


@pytest.fixture
def analyzer():
    return CodeAnalyzer()


@pytest.mark.asyncio
async def test_full_analysis(analyzer):
    """测试完整分析流程"""
    code = """
    import os
    import sqlite3

    def get_user(user_id):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE id = {user_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return result

    def process_items(items):
        results = []
        for item in items:
            for subitem in items:
                if item == subitem:
                    results.append(item)
        return results
    """

    result = await analyzer.analyze_code(code, language="python")

    # 验证结果结构
    assert "analysis_results" in result
    assert "code_review" in result["analysis_results"]
    assert "security" in result["analysis_results"]
    assert "performance" in result["analysis_results"]
    assert "summary" in result


@pytest.mark.asyncio
async def test_selective_analysis(analyzer):
    """测试选择性分析"""
    code = "def hello(): print('Hello')"

    # 只做代码审查
    result = await analyzer.analyze_code(
        code=code,
        language="python",
        analysis_types=["review"],
    )

    assert "code_review" in result["analysis_results"]
    assert "security" not in result["analysis_results"]
    assert "performance" not in result["analysis_results"]


@pytest.mark.asyncio
async def test_batch_analysis(analyzer):
    """测试批量分析"""
    files = [
        {"path": "app.py", "content": "x = 1", "language": "python"},
        {"path": "utils.py", "content": "y = 2", "language": "python"},
    ]

    results = await analyzer.analyze_batch(files)
    assert len(results) == 2
    assert all("analysis_results" in r for r in results)
