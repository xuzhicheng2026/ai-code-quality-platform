"""
测试用例 - 安全检测 Agent
"""

import pytest
from src.agents.security_agent import SecurityAgent


@pytest.fixture
def security_agent():
    return SecurityAgent()


@pytest.mark.asyncio
async def test_quick_scan_sql_injection(security_agent):
    """测试 SQL 注入检测"""
    code = """
    def get_user(user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return execute(query)
    """
    result = await security_agent.analyze(code, language="python")
    assert result["agent"] == "SecurityAgent"
    assert "quick_scan_results" in result


@pytest.mark.asyncio
async def test_quick_scan_command_injection(security_agent):
    """测试命令注入检测"""
    code = """
    import os
    def run_cmd(cmd):
        os.system(cmd)
    """
    result = await security_agent.analyze(code, language="python")
    quick_scan = result["quick_scan_results"]
    # 应该检测到命令注入
    assert len(quick_scan) > 0


@pytest.mark.asyncio
async def test_safe_code(security_agent):
    """测试安全代码"""
    code = """
    def add(a, b):
        return a + b
    """
    result = await security_agent.analyze(code, language="python")
    assert result is not None
    assert "vulnerabilities" in result
