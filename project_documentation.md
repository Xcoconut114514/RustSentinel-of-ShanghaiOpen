
### 2.1 项目背景与价值

**问题陈述：**
Web3 领域（尤其是 Solana 生态）因 Rust 智能合约逻辑复杂，安全漏洞频发，每年导致数十亿美元的资产损失。然而，现有的安全审计面临两大困境：

1. **人工审计昂贵且低效**：由于专业 Rust 审计人员稀缺，中小开发者难以承担高昂费用和漫长的排期。
2. **云端 AI 存在隐私黑洞**：使用 ChatGPT 等通用云端大模型进行辅助审计时，开发者必须上传核心代码，这直接导致**商业机密和未公开漏洞的泄露风险**，对于金融类项目是不可接受的。

**市场/需求分析：**
随着 DeFi 和 RWA（现实资产上链）的爆发，智能合约代码量呈指数级增长。市场上急需一种**“零信任、本地化”**的自动化审计工具。它不仅要能理解复杂的 Rust/Anchor 语法，更必须保证**“代码不出域、数据不落盘”**。这对于注重隐私的机构用户、独立开发者以及黑客松参赛团队来说，是刚性且紧迫的需求。

**解决方案概述：**
RustSentinel 是一个基于**国产沐曦 C500 GPU 算力**的本地化智能审计终端。我们利用 **DeepSeek-R1** 模型的深度逻辑推理能力，构建了一套专用于检测 Rust 权限绕过与逻辑漏洞的 AI 引擎。通过在本地私有化部署，我们实现了在不联网上传代码的前提下，提供达到资深审计员水平的实时代码扫描服务，完美平衡了“安全性”与“隐私性”。

---

### 2.2 技术架构

#### 技术实现

**技术栈**

* **前端**：Gradio (Python Web UI) —— 提供简洁的交互界面与实时流式输出。
* **后端**：Python 3.10 + OpenAI SDK —— 处理业务逻辑与 Prompt 工程。
* **大模型底座**：DeepSeek-R1-Distill (BF16 量化) —— 专注于代码逻辑推理。
* **推理引擎**：vLLM (适配沐曦 C500 NPU) —— 高性能本地推理后端。
* **硬件环境**：**沐曦 MetaX C500 (64GB 显存)** —— 提供国产算力支持。

**主要依赖库**：
`openai`, `gradio`, `vllm`, `torch`, `pydantic`

#### 系统架构图

<img src="https://mermaid.ink/img/pako:eNqVVFtvozgU_iuWnzappQ04gUxbqZtqZ6Q30k7N7CNAg1sTCdjImGSq_Pe1ISTQC31I3g98fOccbL9IaxXggsWvRKJdYwXz17Wc8gX9c5sXJ9n8k62yNEn-2rE_G5ItyZ8H_qfI0s-yY783-w_B2-Q2jZ9P93mZ3qdp9J-sO9m-4W0jLh6J4E-4v03fNrvk8TqZc757I4J_5_8k21cZkU06R9_f50W2-zD7G3j9S-T0QkTSdIt7L0-YF9gH8-4Wc4vG-Q6rC28t5462VvNKGz0rJ6JmZ1wQo52xXJCo2Y1yXDApE7XjVjKua9HqBql4rVmtfR2M9lJ00kY-W2F7qRk7iI2x2grN6Z0V-iAto7rUomN2UaK9tEp2SgWpWW-sUa3kR-W5Fq2x1gZ2WpE-Gvms3khrzEZZY5l-V4_j0jCud8rKkZc63gO_1j0rB957qVkXwJj3yqgD68xGaN-d44L4B0OcsH-X7P4632XxvD_F64fDbrl9-R9c_3Q4HLd5_B0n2Tq5H495lMTZ9sVwG0f5-jC-uX4k5J-k_Z6Xj_t18niYJ6uX_XGfxnF2n-5S_mF7m79Hj__L5Nvl9n6_T-YkfZ3F27_uLpZ1a6c_F5-d_n3g752_n9a8q43p-Xn9FzZ6tT46_0B6c4D_3bV7gN6tD3B3_gA9u8E_Xg-w0V642p2Xz49m80KqD6r_Ww3zS1qP7G6T-9f4Pq9-Z3V0dY2rK4rKz7y4kYxXk5j54Y-Y8Yc_fH78I8L86R5F-e8I8-v0j8Lh0z1e_H-q9k-F658eP1X7p8J_p2r__lX7p8J_p2r_VPifVfu_dFX7p8J_rWo_64X779WwG2J9Y-VIGzloX15eC8W01E6r_k9qL5n5T5fM1R9eKsu9sE-fS5b6aVz0-1XN_rJk9W9T8vOq_b-cKv-nFfvXFPunxL8T3r55aR-d1Fp1_r8lS3X_eN78C461kY8" alt="RustSentinel System Architecture Diagram" width="800">

1. **用户交互层 (User Layer)**：开发者通过 Web 界面输入 Rust/Anchor 源代码。
2. **提示词编排层 (Prompt Layer)**：系统自动封装“安全专家”系统提示词，针对逻辑漏洞、权限校验（Signer Check）进行定向聚焦。
3. **本地推理层 (Inference Layer)**：请求通过内网转发至部署在 **C500 GPU** 上的 vLLM 服务，模型在本地显存中完成推理，**全程不连接外网**。
4. **结果渲染层 (Render Layer)**：以 Markdown 格式实时流式返回漏洞评级、原理分析及修复代码。

#### 核心功能模块

1. **智能合约逻辑扫描模块**：基于 AST（抽象语法树）理解和 DeepSeek 推理能力，专门检测 Solana 合约中特有的“账户所有权校验缺失”和“整数溢出”漏洞。
2. **隐私保护推理通道**：构建基于 `localhost` 的内网推理管道，屏蔽外部网络请求，确保输入的代码仅在本地内存中流转，任务结束后立即释放。
3. **交互式修复建议模块**：不仅发现问题，还能生成经过修正的 Rust 代码片段，帮助开发者通过“对比学习”快速修复漏洞。

---

### 2.3 开源相关信息

**开源协议**：**MIT License**
*理由：MIT 是最宽松的开源协议之一，允许任何人免费使用、修改和分发。这符合我们希望“降低 Web3 安全门槛、赋能独立开发者”的初衷，鼓励更多人基于 RustSentinel 构建自己的安全工具。*

**代码仓库地址**：
[https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen](https://www.google.com/search?q=https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen)

**开源状态**：
[x] **已开源**
*(说明：项目核心的 Prompt 策略、UI 交互逻辑及部署脚本已完全开源；模型权重文件因版权和体积原因引用官方 DeepSeek 链接)*

---

### 2.4 开发进度

**已完成功能**：

* [x] 完成沐曦 C500 环境下的 DeepSeek 模型部署与 vLLM 适配。
* [x] 实现基于 Gradio 的 Web 可视化交互界面。
* [x] 跑通了“Rust 代码输入 -> 本地推理 -> 漏洞报告生成”的完整 MVP 闭环。
* [x] 针对 Solana 经典漏洞（如缺少 Signer 检查）优化了 System Prompt。

**待完善功能**：

* [ ] 支持整个 GitHub 仓库的批量导入与扫描。
* [ ] 集成 RAG（检索增强生成）技术，挂载最新的 Solana 官方安全文档库。
* [ ] 导出 PDF/HTML 格式的正式审计报告。

**遇到的挑战与解决方案**：

* **挑战**：云端环境的端口限制导致 Web 服务无法直接访问。
* **解决方案**：利用 Jupyter Server Proxy 机制配置路由转发，并结合 SSH 隧道技术（Tunneling）实现了公网穿透访问，成功打通了用户与内网算力的连接。

**已知问题与局限性**：

* 当前版本主要针对单文件分析，对于跨文件的复杂逻辑调用链分析能力尚待提升。
* 受限于模型上下文窗口（Context Window），超大型合约（超过 30k tokens）可能需要分段输入。
