# AI Code Quality Platform 使用示例

## 快速开始

### 1. 安装

```bash
pip install -r requirements.txt
```

### 2. 配置 API Keys

复制配置示例文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Keys。

### 3. 运行 API 服务

```bash
python -m src.api.main
```

服务将在 `http://localhost:8000` 启动。

### 4. 使用 API

使用 curl 测试：

```bash
# 健康检查
curl http://localhost:8000/health

# 分析代码
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(): print(\"Hello World\")",
    "language": "python"
  }'
```

## Python SDK 使用

```python
from src.services.code_analyzer import CodeAnalyzer

# 创建分析器
analyzer = CodeAnalyzer()

# 分析代码
code = '''
def calculate_sum(numbers):
    result = 0
    for n in numbers:
        result += n
    return result
'''

result = await analyzer.analyze_code(
    code=code,
    language="python"
)

print(result["summary"])
```

## 输出示例

```json
{
  "language": "python",
  "code_length": 145,
  "analysis_results": {
    "code_review": {
      "agent": "CodeReviewAgent",
      "issues": [...]
    },
    "security": {
      "agent": "SecurityAgent",
      "vulnerabilities": [...]
    },
    "performance": {
      "agent": "PerformanceAgent",
      "recommendations": [...]
    }
  },
  "summary": {
    "total_issues": 3,
    "critical_issues": 0,
    "high_issues": 1,
    "medium_issues": 1,
    "low_issues": 1
  }
}
```
