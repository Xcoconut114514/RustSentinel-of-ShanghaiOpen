# API 文档

## 概述

RustSentinel 提供两种 API 使用方式：
1. **vLLM OpenAI 兼容 API**：标准的 OpenAI Chat Completions API
2. **Python 函数 API**：直接调用 Python 函数

## vLLM OpenAI 兼容 API

### 基础信息

- **Base URL**: `http://localhost:8000/v1`
- **认证**: 不需要（本地部署）
- **协议**: HTTP/HTTPS
- **格式**: JSON

### Chat Completions

创建聊天补全请求以执行代码审计。

**端点**: `POST /v1/chat/completions`

**请求示例**:

```python
import openai

client = openai.OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[
        {
            "role": "system",
            "content": "你是一个 Solana 智能合约安全审计专家。"
        },
        {
            "role": "user",
            "content": "请审计这段代码：\n\n[你的 Rust 代码]"
        }
    ],
    temperature=0.1,
    max_tokens=2048,
    stream=False
)

print(response.choices[0].message.content)
```

**请求参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `model` | string | 是 | - | 模型名称，使用 `deepseek-audit` |
| `messages` | array | 是 | - | 消息列表 |
| `temperature` | float | 否 | 1.0 | 采样温度（0.0-2.0），建议 0.1-0.3 |
| `max_tokens` | integer | 否 | 无限 | 最大生成 token 数 |
| `stream` | boolean | 否 | false | 是否启用流式输出 |
| `top_p` | float | 否 | 1.0 | 核采样参数 |
| `presence_penalty` | float | 否 | 0.0 | 存在惩罚 |
| `frequency_penalty` | float | 否 | 0.0 | 频率惩罚 |

**响应示例**:

```json
{
  "id": "cmpl-xxxxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "deepseek-audit",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "### 风险等级\n严重\n\n### 发现的漏洞\n..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 456,
    "total_tokens": 579
  }
}
```

### 流式输出

启用 `stream=True` 以获得实时响应：

```python
response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[...],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 错误处理

**常见错误码**:

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |
| 503 | 服务暂时不可用 |

**错误响应示例**:

```json
{
  "error": {
    "message": "Invalid request: ...",
    "type": "invalid_request_error",
    "code": "invalid_parameter"
  }
}
```

## Python 函数 API

### smart_audit()

执行智能审计的主函数。

**函数签名**:

```python
def smart_audit(code_snippet: str) -> str
```

**参数**:

- `code_snippet` (str): 待审计的 Rust 源代码

**返回值**:

- str: Markdown 格式的审计报告

**异常**:

- `Exception`: 审计过程中的任何错误

**示例**:

```python
from src.app_gradio import smart_audit

rust_code = """
use anchor_lang::prelude::*;

#[program]
pub mod my_contract {
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        // 你的代码
    }
}
"""

try:
    report = smart_audit(rust_code)
    print(report)
except Exception as e:
    print(f"审计失败: {e}")
```

## 使用建议

### 温度（Temperature）设置

- **0.0-0.3**: 推荐用于安全审计（更加确定和一致的输出）
- **0.3-0.7**: 平衡创造性和一致性
- **0.7-1.0**: 更有创造性，但可能不够精确

### 系统提示词（System Prompt）

为了获得最佳审计结果，使用专业的系统提示词：

```python
system_prompt = """
你是一个资深的 Solana 智能合约安全审计专家。
请重点检测：
1. Signer 检查缺失
2. 账户所有权验证缺失
3. 整数溢出/下溢
4. 重入攻击
5. 逻辑错误

输出格式：
- 风险等级
- 漏洞描述
- 攻击原理
- 修复建议
- 修复代码
"""
```

### 上下文管理

对于复杂的合约，可能需要多轮对话：

```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"请审计这段代码：\n{code}"},
]

response = client.chat.completions.create(
    model="deepseek-audit",
    messages=messages
)

# 继续对话
messages.append({
    "role": "assistant", 
    "content": response.choices[0].message.content
})
messages.append({
    "role": "user", 
    "content": "请详细解释第一个漏洞的攻击原理"
})

# 发送第二轮请求
response2 = client.chat.completions.create(
    model="deepseek-audit",
    messages=messages
)
```

## 性能优化

### 批处理

审计多个文件时，可以并发发送请求：

```python
import asyncio
from openai import AsyncOpenAI

async def audit_file(client, code):
    response = await client.chat.completions.create(
        model="deepseek-audit",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": code}
        ]
    )
    return response.choices[0].message.content

async def batch_audit(files):
    client = AsyncOpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8000/v1"
    )
    
    tasks = [audit_file(client, code) for code in files]
    results = await asyncio.gather(*tasks)
    return results

# 使用示例
codes = [code1, code2, code3]
reports = asyncio.run(batch_audit(codes))
```

### 超时设置

为长时间运行的请求设置超时：

```python
from openai import OpenAI
import httpx

client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1",
    timeout=httpx.Timeout(300.0)  # 5分钟超时
)
```

## 限流和配额

本地部署版本没有请求限制，但受限于：

- GPU 显存容量
- 并发处理能力（默认最大 32 个并发请求）
- 序列长度限制（默认 8192 tokens）

## 健康检查

检查服务是否正常运行：

```bash
curl http://localhost:8000/health
```

或使用 Python：

```python
import requests

try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        print("服务正常运行")
    else:
        print(f"服务异常: {response.status_code}")
except Exception as e:
    print(f"无法连接到服务: {e}")
```

## 版本信息

查询模型和服务信息：

```bash
curl http://localhost:8000/v1/models
```

## 更多资源

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [vLLM 文档](https://docs.vllm.ai/)
- [示例代码](../examples/)

---

如有问题，请查看 [常见问题](deployment.md#常见问题解答) 或提交 Issue。
