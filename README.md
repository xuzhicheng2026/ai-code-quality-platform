# AI 代码质量分析平台

基于多 Agent 架构的企业级 AI 代码质量分析平台，支持自动化代码审查、安全漏洞检测和性能优化建议。

## 项目简介

本项目实现了一套企业级 AI 驱动的代码质量分析系统，基于多 Agent 架构，通过智能路由选择最合适的模型处理不同类型的代码分析任务。

### 核心功能

- 🤖 **智能代码审查** - 自动分析代码规范、潜在 Bug 和代码风格问题
- 🔒 **安全漏洞检测** - 识别常见安全漏洞和潜在风险
- ⚡ **性能优化建议** - 提供代码性能改进建议
- 🔀 **多模型路由** - 支持 Claude、GPT、DeepSeek 等多模型智能路由

### 技术架构

- **多 Agent 协作**：CodeReviewAgent、SecurityAgent、PerformanceAgent
- **LLM 路由服务**：智能选择最合适的 AI 模型
- **微服务架构**：支持私有化部署和云端 SaaS 模式

## 快速开始

### 安装依赖

\\\ash
pip install -r requirements.txt
\\\

### 配置环境变量

\\\ash
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
\\\

### 启动服务

\\\ash
python src/api/main.py
\\\

## License

MIT License
