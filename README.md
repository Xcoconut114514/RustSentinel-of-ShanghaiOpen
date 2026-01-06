# 🛡️ RustSentinel

> 基于沐曦 C500 算力的 Rust 智能合约本地化隐私安全审计终端

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 📖 项目简介

RustSentinel 是一个专为 Solana/Rust 智能合约设计的本地化安全审计工具。基于 **国产沐曦 C500 GPU** 算力和 **DeepSeek-R1** 深度推理模型，实现了在完全本地环境下对智能合约进行专业级安全审计，确保代码隐私的同时提供高质量的漏洞检测服务。

### 核心特性

- 🔒 **绝对隐私**：全本地化推理，代码永不出域，消除泄密隐患
- 🎯 **逻辑专精**：专攻 Rust/Anchor 框架特有的权限绕过与逻辑缺陷
- ⚡ **实时审计**：基于 C500 GPU 的高性能推理引擎，秒级响应
- 🌐 **友好界面**：Gradio/Streamlit 可视化交互，支持流式输出
- 📊 **专业报告**：输出包含漏洞等级、攻击原理和修复建议的 Markdown 报告

### 解决的问题

针对 Web3 领域（特别是 Solana/Rust 生态）智能合约漏洞频发导致巨额资产损失的痛点：

1. **人工审计昂贵且低效**：专业 Rust 审计人员稀缺，中小开发者难以承担高昂费用
2. **云端 AI 存在隐私风险**：使用云端大模型需上传核心代码，存在商业机密泄露风险
3. **通用模型漏报率高**：难以精准识别 Rust/Anchor 框架特有的深层逻辑漏洞

### 目标用户

- Solana/Rust 智能合约开发者
- Web3 安全研究员
- 区块链项目初创团队
- 黑客松参赛团队

## 🚀 快速开始

### 前置要求

- Python 3.10 或更高版本
- 沐曦 C500 GPU（64GB 显存推荐）或其他支持的 GPU
- 至少 100GB 可用磁盘空间（用于模型存储）

### 一键启动

```bash
# 1. 克隆仓库
git clone https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen.git
cd RustSentinel-of-ShanghaiOpen

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动 vLLM 推理服务（需在支持的 GPU 环境）
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --dtype bfloat16 \
    --port 8000 \
    --model-name deepseek-audit

# 4. 启动 Web 界面（新终端）
python src/app_gradio.py
```

访问 `http://localhost:8501` 开始使用！

## 📦 安装部署指南

### 方法一：本地部署（推荐）

详细部署步骤请参考 [部署文档](docs/deployment.md)

#### 第一步：环境准备

```bash
# 创建 Python 虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 第二步：模型下载

```bash
# 方法 1：使用 HuggingFace Hub
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-7B

# 方法 2：使用 ModelScope（国内推荐）
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('deepseek-ai/DeepSeek-R1-Distill-Qwen-7B')"
```

#### 第三步：启动服务

```bash
# 终端 1：启动推理引擎
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.9 \
    --port 8000

# 终端 2：启动 Web 界面
cd src
python app_gradio.py
```

### 方法二：Docker 部署

```bash
# 构建镜像
docker build -t rustsentinel:latest -f docker/Dockerfile .

# 运行容器
docker run -d \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    rustsentinel:latest
```

详细配置请参考 [Docker 部署文档](docs/docker-deployment.md)

## 💡 使用示例

### 命令行审计

```python
from openai import OpenAI

# 连接本地模型
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

# 待审计的代码
rust_code = """
use anchor_lang::prelude::*;
#[program]
pub mod bank {
    use super::*;
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        let from = &mut ctx.accounts.from;
        let to = &mut ctx.accounts.to;
        **from.to_account_info().try_borrow_mut_lamports()? -= amount;
        **to.to_account_info().try_borrow_mut_lamports()? += amount;
        Ok(())
    }
}
"""

# 发起审计
response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[
        {"role": "system", "content": "你是一个资深的 Solana 智能合约安全审计专家。请分析代码漏洞。"},
        {"role": "user", "content": f"请审计这段代码：\n\n{rust_code}"}
    ],
    temperature=0.1
)

print(response.choices[0].message.content)
```

### Web 界面使用

1. 访问 `http://localhost:8501`
2. 在左侧文本框粘贴 Rust 代码
3. 点击"🚀 开始审计"按钮
4. 右侧实时显示审计报告

更多示例请参考 [examples](examples/) 目录。

## 📚 API 文档

### 核心 API

#### `smart_audit(code_snippet: str) -> str`

对输入的 Rust 代码进行安全审计。

**参数：**
- `code_snippet` (str): 待审计的 Rust 源代码

**返回：**
- str: Markdown 格式的审计报告，包含：
  - 风险等级（严重/高危/中危/低危）
  - 漏洞描述
  - 攻击原理
  - 修复建议和代码

**示例：**
```python
from src.app_gradio import smart_audit

report = smart_audit("""
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        // 缺少权限检查的代码
    }
""")
print(report)
```

### 系统提示词定制

可以通过修改 `config/system_prompt.txt` 来定制审计行为：

```python
system_prompt = """
你是一个智能合约安全专家，专注于：
1. 权限绕过漏洞检测
2. 整数溢出/下溢检测
3. 重入攻击检测
4. 逻辑错误检测
"""
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！无论是报告 bug、提出新功能建议，还是提交代码改进。

### 如何贡献

1. **Fork 本仓库**
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **开启 Pull Request**

### 开发规范

- 遵循 PEP 8 Python 代码规范
- 为新功能添加相应的测试用例
- 更新相关文档
- 提交信息使用中文，格式清晰

### 报告问题

如果您发现 bug 或有功能建议，请：

1. 在 [Issues](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues) 中搜索是否已有相关问题
2. 如果没有，创建新的 Issue，并提供：
   - 问题的详细描述
   - 复现步骤
   - 预期行为和实际行为
   - 系统环境信息

## 📄 许可证信息

本项目采用 **MIT License** 开源协议。

这意味着您可以：
- ✅ 自由使用本项目
- ✅ 修改源代码
- ✅ 分发原始或修改版本
- ✅ 用于商业目的

详细内容请查看 [LICENSE](LICENSE) 文件。

## 📞 联系我们

- **项目负责人**: coconut
- **电子邮箱**: 2819404727@qq.com
- **手机**: 18964592960
- **GitHub**: [@Xcoconut114514](https://github.com/Xcoconut114514)

## 🙏 致谢

- 感谢 [沐曦集成电路](https://www.metax-tech.com/) 提供的 C500 GPU 算力支持
- 感谢 [DeepSeek](https://www.deepseek.com/) 团队开源的优秀推理模型
- 感谢开源社区的所有贡献者

## 🗺️ 项目路线图

### 已完成 ✅
- [x] 基于 C500 的 DeepSeek 模型部署
- [x] Gradio Web 可视化界面
- [x] 单文件代码审计功能
- [x] Solana 经典漏洞检测优化

### 进行中 🚧
- [ ] 整个 GitHub 仓库批量扫描
- [ ] RAG 检索增强（挂载 Solana 安全文档库）
- [ ] PDF/HTML 格式审计报告导出

### 计划中 📅
- [ ] VS Code 插件集成
- [ ] CI/CD 流水线集成
- [ ] 多语言合约支持（Move、Cairo 等）
- [ ] 漏洞知识库构建

## 📊 技术架构

```
RustSentinel
├── 用户交互层 (Gradio/Streamlit)
├── Prompt 编排层 (System Prompt)
├── 本地推理层 (vLLM + DeepSeek-R1)
└── 硬件加速层 (沐曦 C500 GPU)
```

详细架构说明请参考 [技术文档](docs/architecture.md)。

---

⭐ 如果这个项目对您有帮助，欢迎 Star 支持！
