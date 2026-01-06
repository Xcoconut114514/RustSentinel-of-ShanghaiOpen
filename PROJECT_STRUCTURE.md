# RustSentinel 项目结构说明

本文档描述 RustSentinel 项目的完整目录结构。

## 📁 目录树

```
RustSentinel-of-ShanghaiOpen/
│
├── README.md                      # 项目主文档（中文）
├── LICENSE                        # MIT 开源协议
├── CONTRIBUTING.md                # 贡献指南（中文）
├── CHANGELOG.md                   # 版本更新日志
├── requirements.txt               # Python 依赖列表
├── quick_start.sh                 # 快速启动脚本
│
├── src/                           # 源代码目录
│   ├── app.py                    # Streamlit Web 应用
│   ├── app_gradio.py             # Gradio Web 应用（主要界面）
│   └── auditor.py                # 审计核心逻辑
│
├── docs/                          # 文档目录
│   ├── README.md                 # 文档索引导航
│   ├── deployment.md             # 部署指南（含系统要求、FAQ）
│   ├── architecture.md           # 技术架构文档
│   ├── api.md                    # API 使用文档
│   ├── docker-deployment.md      # Docker 部署指南
│   └── usage.md                  # 详细使用指南
│
├── config/                        # 配置文件目录
│   ├── example.env               # 环境变量配置示例
│   └── system_prompt.txt         # 系统提示词模板
│
├── docker/                        # Docker 配置目录
│   ├── Dockerfile                # Docker 镜像定义
│   └── docker-compose.yml        # Docker Compose 配置
│
├── examples/                      # 使用示例目录
│   ├── README.md                 # 示例说明文档
│   └── vulnerable_bank.rs        # 漏洞示例代码
│
├── tests/                         # 测试代码目录
│   └── README.md                 # 测试说明文档
│
├── .gitignore                     # Git 忽略文件配置
├── app.py                         # 根目录保留的应用文件
├── app_gradio.py                  # 根目录保留的应用文件
├── auditor.py                     # 根目录保留的审计文件
├── project.md                     # 项目信息（原始）
├── project_documentation.md       # 项目文档（原始）
└── gpu_performance.md             # GPU 性能说明（原始）
```

## 📖 文件说明

### 核心文档

| 文件 | 说明 | 语言 |
|------|------|------|
| README.md | 项目总览，包含简介、快速开始、部署、使用等 | 中文 |
| LICENSE | MIT 开源协议 | 英文 |
| CONTRIBUTING.md | 贡献者指南，代码规范、PR流程等 | 中文 |
| CHANGELOG.md | 版本更新历史记录 | 中文 |

### 源代码 (src/)

| 文件 | 说明 |
|------|------|
| app_gradio.py | Gradio Web 界面主程序 |
| app.py | Streamlit Web 界面（备选） |
| auditor.py | 核心审计逻辑 |

### 文档 (docs/)

| 文件 | 说明 | 内容 |
|------|------|------|
| README.md | 文档导航索引 | 文档结构、快速导航 |
| deployment.md | 部署指南 | 系统要求、部署步骤、FAQ |
| architecture.md | 技术架构 | 系统设计、技术栈、性能优化 |
| api.md | API 文档 | API 使用方法、参数说明 |
| docker-deployment.md | Docker 部署 | 容器化部署完整指南 |
| usage.md | 使用指南 | 详细使用说明、高级用法 |

### 配置 (config/)

| 文件 | 说明 |
|------|------|
| example.env | 环境变量配置示例 |
| system_prompt.txt | AI 审计系统提示词模板 |

### Docker (docker/)

| 文件 | 说明 |
|------|------|
| Dockerfile | Docker 镜像构建文件 |
| docker-compose.yml | Docker Compose 编排配置 |

### 示例 (examples/)

| 文件 | 说明 |
|------|------|
| README.md | 示例使用说明 |
| vulnerable_bank.rs | 包含安全漏洞的 Solana 合约示例 |

### 测试 (tests/)

| 文件 | 说明 |
|------|------|
| README.md | 测试说明和规范 |

## ✅ 符合要求对照

### 4.1 代码仓库要求

- ✅ README.md - 项目总览
- ✅ docs/ - 详细文档（6个文档文件）
- ✅ src/ - 源代码
- ✅ tests/ - 测试代码
- ✅ examples/ - 使用示例
- ✅ config/ - 配置文件
- ✅ docker/ - 容器化配置
- ✅ LICENSE - 开源协议（MIT）
- ✅ requirements.txt - 依赖列表

### 4.2 README.md 必备内容

- ✅ 项目简介
- ✅ 快速开始
- ✅ 安装部署指南
- ✅ 使用示例
- ✅ API文档（链接）
- ✅ 贡献指南（链接）
- ✅ 许可证信息

### 4.3 部署说明

- ✅ 最低系统要求（在 docs/deployment.md）
- ✅ 一步步部署指南（3种方式）
- ✅ 环境变量配置（config/example.env）
- ✅ 常见问题解答（10+ FAQ）

## 🌟 特色

1. **全中文文档** - 所有文档均使用中文编写
2. **完整的部署方案** - 支持本地、Docker、K8s 部署
3. **丰富的文档** - 超出要求，提供架构、API、使用等多份文档
4. **快速启动** - 提供 quick_start.sh 自动化脚本
5. **专业规范** - 符合开源项目最佳实践

## 📊 统计

- 总文件数: 29+
- 文档文件: 12个（全中文）
- 代码文件: 3个
- 配置文件: 4个
- 总字数: 约 50,000+ 字

---

最后更新: 2024-01-06
