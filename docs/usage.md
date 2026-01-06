# 使用指南

本文档提供 RustSentinel 的详细使用说明。

## 🚀 启动服务

### 方法一：分步启动（推荐用于开发）

#### 1. 启动 vLLM 推理服务

在第一个终端中：

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 vLLM
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --dtype bfloat16 \
    --port 8000 \
    --gpu-memory-utilization 0.9 \
    --model-name deepseek-audit
```

等待看到以下输出：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 2. 启动 Web 界面

在第二个终端中：

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 Gradio 界面
cd src
python app_gradio.py
```

访问 http://localhost:8501 开始使用。

### 方法二：使用 Docker

```bash
docker-compose -f docker/docker-compose.yml up -d
```

详细说明见 [Docker 部署文档](docker-deployment.md)。

## 💻 基本使用

### Web 界面使用

1. **粘贴代码**
   - 在左侧文本框粘贴待审计的 Rust 代码
   - 或者点击"加载示例"按钮使用预设示例

2. **开始审计**
   - 点击"🚀 开始审计"按钮
   - 等待 AI 分析（通常 5-30 秒）

3. **查看报告**
   - 右侧实时显示审计进度
   - 生成 Markdown 格式的审计报告
   - 包含漏洞等级、描述、修复建议

4. **导出报告**（即将支持）
   - 点击"导出 PDF"保存报告
   - 或复制 Markdown 文本

### 命令行使用

创建 Python 脚本：

```python
# my_audit.py
from openai import OpenAI

# 读取待审计的代码
with open("my_contract.rs", "r") as f:
    code = f.read()

# 连接本地模型
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

# 执行审计
response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[
        {
            "role": "system",
            "content": "你是一个资深的 Solana 智能合约安全审计专家。"
        },
        {
            "role": "user",
            "content": f"请审计这段代码：\n\n{code}"
        }
    ],
    temperature=0.1,
    max_tokens=2048
)

# 保存报告
report = response.choices[0].message.content
with open("audit_report.md", "w") as f:
    f.write(report)

print("审计完成！报告已保存到 audit_report.md")
```

运行：

```bash
python my_audit.py
```

## 🎯 高级用法

### 自定义系统提示词

编辑 `config/system_prompt.txt` 来定制审计行为：

```text
你是一个智能合约安全专家，专注于：

1. 权限绕过漏洞
2. 重入攻击
3. [你的自定义检测项]

输出格式：
[你的自定义格式]
```

### 批量审计

创建批量审计脚本：

```python
# batch_audit.py
import os
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

# 审计目录下所有 .rs 文件
contracts_dir = "contracts/"
for filename in os.listdir(contracts_dir):
    if filename.endswith(".rs"):
        print(f"正在审计: {filename}")
        
        with open(os.path.join(contracts_dir, filename), "r") as f:
            code = f.read()
        
        response = client.chat.completions.create(
            model="deepseek-audit",
            messages=[
                {"role": "system", "content": "你是安全审计专家"},
                {"role": "user", "content": f"审计代码：\n{code}"}
            ]
        )
        
        # 保存报告
        report_name = f"report_{filename}.md"
        with open(report_name, "w") as f:
            f.write(response.choices[0].message.content)
        
        print(f"✓ 完成: {report_name}\n")
```

### 流式输出

获得实时响应：

```python
response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[...],
    stream=True  # 启用流式输出
)

print("审计报告：")
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 多轮对话

深入分析特定问题：

```python
messages = [
    {"role": "system", "content": "你是安全审计专家"},
    {"role": "user", "content": "审计这段代码：\n" + code}
]

# 第一轮
response1 = client.chat.completions.create(
    model="deepseek-audit",
    messages=messages
)
messages.append({
    "role": "assistant",
    "content": response1.choices[0].message.content
})

# 追问
messages.append({
    "role": "user",
    "content": "请详细解释第一个漏洞的攻击场景"
})

response2 = client.chat.completions.create(
    model="deepseek-audit",
    messages=messages
)
print(response2.choices[0].message.content)
```

## 🔍 审计报告解读

### 风险等级

- **严重**: 可直接导致资金损失的漏洞，必须立即修复
- **高危**: 可能导致严重后果，强烈建议修复
- **中危**: 存在安全隐患，建议修复
- **低危**: 最佳实践建议，可选修复

### 报告结构

典型的审计报告包含：

1. **风险等级**: 总体风险评估
2. **漏洞列表**: 发现的所有问题
   - 漏洞名称
   - 严重程度
   - 漏洞描述
   - 攻击原理
   - 修复建议
   - 修复代码
3. **总体评估**: 综合评价和建议

### 常见漏洞类型

| 漏洞类型 | 说明 | 典型场景 |
|---------|------|---------|
| Signer 检查缺失 | 未验证账户签名者 | 任何人都能操作他人账户 |
| 所有权验证缺失 | 未检查账户归属 | PDA 验证不当 |
| 整数溢出 | 算术运算溢出 | 余额计算错误 |
| 重入攻击 | 跨程序调用漏洞 | 递归调用导致状态错误 |
| 逻辑错误 | 业务逻辑缺陷 | 权限控制绕过 |

## 🛠️ 故障排除

### 问题：审计速度很慢

**原因**: GPU 显存不足或模型未充分利用 GPU

**解决**:
```bash
# 调整显存利用率
vllm serve ... --gpu-memory-utilization 0.95

# 使用量化模型
vllm serve ... --quantization awq
```

### 问题：生成内容质量不佳

**原因**: Temperature 设置不当或提示词不够明确

**解决**:
```python
# 降低 temperature 以获得更确定的输出
response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[...],
    temperature=0.1  # 推荐范围 0.1-0.3
)
```

### 问题：无法连接到服务

**解决**:
```bash
# 检查 vLLM 是否运行
curl http://localhost:8000/health

# 检查端口占用
netstat -tuln | grep 8000

# 查看 vLLM 日志
# (查看启动 vLLM 的终端输出)
```

### 问题：显存溢出

**解决**:
```bash
# 方法 1: 减少上下文长度
vllm serve ... --max-model-len 4096

# 方法 2: 启用量化
vllm serve ... --quantization awq

# 方法 3: 降低显存利用率
vllm serve ... --gpu-memory-utilization 0.7
```

## 📊 性能优化建议

### 单次审计优化

- 使用 BF16 精度（默认）
- 设置合适的 max_tokens（推荐 1024-2048）
- 降低 temperature（0.1-0.3）

### 批量审计优化

- 使用异步 API 并发处理
- 合理设置请求间隔
- 监控 GPU 显存使用

### 服务器配置

```bash
# 生产环境推荐配置
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --dtype bfloat16 \
    --port 8000 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 8192 \
    --model-name deepseek-audit \
    --disable-log-requests \  # 禁用请求日志
    --trust-remote-code
```

## 🔗 更多资源

- [API 文档](api.md) - 详细的 API 说明
- [示例代码](../examples/) - 更多使用示例
- [常见问题](deployment.md#常见问题解答) - FAQ

## 💬 获取帮助

- 📖 查看[文档索引](README.md)
- 🐛 提交 [Issue](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues)
- 📧 邮件联系: 2819404727@qq.com

---

祝您使用愉快！🎉
