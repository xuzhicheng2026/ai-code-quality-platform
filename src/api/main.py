"""
FastAPI 主程序 - 提供 RESTful API 服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from loguru import logger

from src.services.code_analyzer import CodeAnalyzer

# 配置日志
logger.add("logs/api.log", rotation="500 MB", level="INFO")

# 创建 FastAPI 应用
app = FastAPI(
    title="AI Code Quality Platform API",
    description="基于多 Agent 架构的代码质量分析平台",
    version="1.0.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化分析器
analyzer = CodeAnalyzer()


# 请求模型
class CodeAnalysisRequest(BaseModel):
    """代码分析请求"""
    code: str
    language: str = "python"
    analysis_types: Optional[List[str]] = None


class BatchAnalysisRequest(BaseModel):
    """批量分析请求"""
    files: List[dict]  # [{"path": str, "content": str, "language": str}]


# 响应模型
class CodeAnalysisResponse(BaseModel):
    """代码分析响应"""
    success: bool
    data: dict
    message: str = ""


# API 端点
@app.get("/")
async def root():
    """API 根路径"""
    return {
        "name": "AI Code Quality Platform",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    分析单段代码

    - **code**: 要分析的代码
    - **language**: 编程语言 (python, javascript, etc.)
    - **analysis_types**: 分析类型列表 ["review", "security", "performance"]
    """
    try:
        logger.info(f"Analyzing code: {len(request.code)} chars")

        result = await analyzer.analyze_code(
            code=request.code,
            language=request.language,
            analysis_types=request.analysis_types,
        )

        return CodeAnalysisResponse(
            success=True,
            data=result,
            message="Analysis completed successfully",
        )

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/batch", response_model=CodeAnalysisResponse)
async def analyze_batch(request: BatchAnalysisRequest):
    """
    批量分析多个文件

    - **files**: 文件列表 [{"path": str, "content": str, "language": str}]
    """
    try:
        logger.info(f"Batch analyzing {len(request.files)} files")

        results = await analyzer.analyze_batch(files=request.files)

        return CodeAnalysisResponse(
            success=True,
            data={"results": results, "total_files": len(results)},
            message=f"Analyzed {len(results)} files",
        )

    except Exception as e:
        logger.error(f"Batch analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/capabilities")
async def get_capabilities():
    """获取平台能力"""
    return {
        "agents": ["CodeReviewAgent", "SecurityAgent", "PerformanceAgent"],
        "supported_languages": ["python", "javascript", "typescript", "java", "go"],
        "analysis_types": {
            "review": "代码审查和质量分析",
            "security": "安全漏洞检测",
            "performance": "性能优化建议",
        },
    }


def main():
    """启动服务"""
    logger.info("Starting AI Code Quality Platform API...")
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
