# 文档索引

欢迎来到 RustSentinel 文档中心！

## 📚 快速导航

### 新手入门

1. **[README.md](../README.md)** - 项目总览和快速开始
2. **[部署指南](deployment.md)** - 详细的安装部署步骤
3. **[使用示例](../examples/README.md)** - 实际使用案例

### 技术文档

4. **[技术架构](architecture.md)** - 系统设计和技术栈
5. **[API 文档](api.md)** - API 使用说明和示例
6. **[Docker 部署](docker-deployment.md)** - 容器化部署指南

### 开发指南

7. **[贡献指南](../CONTRIBUTING.md)** - 如何为项目做贡献
8. **[测试文档](../tests/README.md)** - 测试说明和规范
9. **[更新日志](../CHANGELOG.md)** - 版本更新记录

### 配置参考

10. **[环境变量配置](../config/example.env)** - 环境变量说明
11. **[系统提示词](../config/system_prompt.txt)** - 审计提示词模板

## 📖 文档结构

```
RustSentinel/
├── README.md                    # 项目主文档
├── LICENSE                      # MIT 开源协议
├── CONTRIBUTING.md              # 贡献指南
├── CHANGELOG.md                 # 更新日志
│
├── docs/                        # 详细文档目录
│   ├── README.md               # 文档索引（本文件）
│   ├── deployment.md           # 部署指南
│   ├── architecture.md         # 技术架构
│   ├── api.md                  # API 文档
│   └── docker-deployment.md    # Docker 部署
│
├── src/                         # 源代码
│   ├── app.py                  # Streamlit 应用
│   ├── app_gradio.py           # Gradio 应用
│   └── auditor.py              # 审计核心逻辑
│
├── tests/                       # 测试代码
│   └── README.md               # 测试说明
│
├── examples/                    # 使用示例
│   ├── README.md               # 示例说明
│   └── vulnerable_bank.rs      # 漏洞示例代码
│
├── config/                      # 配置文件
│   ├── example.env             # 环境变量示例
│   └── system_prompt.txt       # 系统提示词
│
└── docker/                      # Docker 配置
    ├── Dockerfile              # Docker 镜像定义
    └── docker-compose.yml      # Docker Compose 配置
```

## 🎯 按需求查找

### 我想部署 RustSentinel
1. 阅读 [部署指南](deployment.md)
2. 查看 [Docker 部署](docker-deployment.md)（可选）
3. 参考 [环境变量配置](../config/example.env)

### 我想使用 API
1. 阅读 [API 文档](api.md)
2. 查看 [使用示例](../examples/README.md)
3. 运行示例代码

### 我想贡献代码
1. 阅读 [贡献指南](../CONTRIBUTING.md)
2. 了解 [技术架构](architecture.md)
3. 编写测试（参考 [测试文档](../tests/README.md)）

### 我遇到了问题
1. 查看 [部署指南的 FAQ](deployment.md#常见问题解答)
2. 搜索 [GitHub Issues](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues)
3. 创建新的 Issue

## 🔗 外部资源

- [DeepSeek 官网](https://www.deepseek.com/)
- [vLLM 文档](https://docs.vllm.ai/)
- [Gradio 文档](https://www.gradio.app/docs)
- [Solana 官方文档](https://docs.solana.com/)
- [Anchor 框架文档](https://www.anchor-lang.com/)

## 📝 文档贡献

发现文档错误或想改进文档？

1. Fork 仓库
2. 修改文档
3. 提交 Pull Request

感谢您的贡献！

---

最后更新：2024-01-06
