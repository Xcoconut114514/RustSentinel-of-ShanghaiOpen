# 更新日志

本文档记录 RustSentinel 项目的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 完整的项目文档结构
- README.md 中文文档
- 部署指南和 FAQ
- Docker 部署支持
- API 文档
- 贡献指南
- MIT 开源协议

### 改进
- 重组项目目录结构
- 更新 .gitignore 文件
- 添加环境变量配置示例

## [0.1.0] - 2024-01-06

### 新增
- 基于沐曦 C500 GPU 的本地化推理引擎
- Gradio Web 可视化界面
- Streamlit 备用界面
- DeepSeek-R1-Distill 模型集成
- Solana/Rust 智能合约审计功能
- 专业的安全审计系统提示词
- 漏洞示例代码（vulnerable_bank.rs）

### 功能特性
- 实时流式输出审计报告
- Markdown 格式报告生成
- 权限绕过漏洞检测
- 账户所有权验证检测
- 整数溢出检测

### 技术栈
- Python 3.10+
- vLLM 推理引擎
- OpenAI SDK
- Gradio 4.x
- DeepSeek-R1-Distill-Qwen-7B

---

## 版本说明

### 版本格式

版本号格式：`主版本号.次版本号.修订号`

- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 更新类型

- **新增**: 新功能
- **改进**: 对现有功能的改进
- **修复**: Bug 修复
- **弃用**: 即将移除的功能
- **移除**: 已移除的功能
- **安全**: 安全相关的修复

---

[未发布]: https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/releases/tag/v0.1.0
