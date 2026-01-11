# RustSentinel AI 助手后端服务说明

## 快速启动

### 方法一：使用启动脚本（推荐）
```bash
启动AI助手后端.bat
```

### 方法二：手动命令
```bash
# 1. 激活虚拟环境
call venv\Scripts\activate

# 2. 安装依赖（首次运行）
pip install mysql-connector-python requests flask flask-cors

# 3. 启动服务
python simple_server_ollama_with_db.py
```

## 服务端点

### 1. 智能客服 API（新增）
```
POST http://localhost:8000/v1/assistant/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "如何使用 RustSentinel？"
    }
  ]
}
```

**用途：** AI 智能客服，回答用户关于平台的问题

**特点：**
- 快速响应（60秒超时）
- 中文优化
- 专门的客服提示词
- Temperature: 0.7（更自然的对话）
- Max tokens: 512（简洁回答）

### 2. 代码审计 API（原有）
```
POST http://localhost:8000/v1/chat/completions
Content-Type: application/json

{
  "messages": [
    {
      "role": "system",
      "content": "你是 Rust 安全审计专家..."
    },
    {
      "role": "user",
      "content": "审计这段代码：..."
    }
  ]
}
```

**用途：** 深度代码安全审计

**特点：**
- 深度分析（300秒超时）
- Temperature: 0.2（更准确）
- Max tokens: 2048（详细报告）
- 自动保存到数据库

### 3. 审计历史 API
```
GET http://localhost:8000/api/history?page=1&page_size=10
GET http://localhost:8000/api/history/{id}
DELETE http://localhost:8000/api/history/{id}
```

### 4. 健康检查 API
```
GET http://localhost:8000/health
```

返回：
```json
{
  "status": "ok",
  "engine": "Ollama",
  "model": "deepseek-coder:6.7b",
  "ollama_status": "running",
  "database": "ok (10 records)"
}
```

## 配置说明

### Ollama 配置
```python
# 在 simple_server_ollama_with_db.py 中
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-coder:6.7b"
```

### 数据库配置（可选）
```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',  # 修改为你的密码
    'database': 'rustsentinel',
    'port': 3306
}
```

**注意：** 如果不需要数据库功能，服务仍可正常运行，只是不会保存审计历史。

## 前置要求

### 1. Ollama
```bash
# 下载安装
https://ollama.com/download

# 下载模型
ollama pull deepseek-coder:6.7b

# 检查状态
ollama list
```

### 2. Python 虚拟环境
```bash
# 如果没有虚拟环境，创建一个
python -m venv venv
```

### 3. MySQL（可选）
```sql
-- 创建数据库
CREATE DATABASE rustsentinel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## API 对比

| 特性 | 代码审计 API | 智能客服 API |
|------|------------|------------|
| 端点 | `/v1/chat/completions` | `/v1/assistant/chat` |
| 用途 | 深度代码分析 | 快速问答 |
| 超时 | 300秒 | 60秒 |
| Temperature | 0.2 | 0.7 |
| Max Tokens | 2048 | 512 |
| 保存数据库 | ✅ | ❌ |
| 系统提示词 | 代码审计专家 | 客服助手 |

## 测试命令

### 测试智能客服
```bash
curl -X POST http://localhost:8000/v1/assistant/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"如何使用 RustSentinel？\"}]}"
```

### 测试健康检查
```bash
curl http://localhost:8000/health
```

## 故障排除

### 问题 1：Ollama 连接失败
```
错误: 无法连接到 Ollama
```

**解决：**
1. 确保 Ollama 正在运行
2. 检查端口 11434 是否被占用
3. 重启 Ollama 服务

### 问题 2：模型未找到
```
错误: model 'deepseek-coder:6.7b' not found
```

**解决：**
```bash
ollama pull deepseek-coder:6.7b
```

### 问题 3：数据库连接失败
```
警告: 数据库初始化失败
```

**解决：**
1. 检查 MySQL 是否运行
2. 验证数据库配置
3. 创建数据库 `rustsentinel`

**注意：** 数据库失败不影响 AI 功能，只是不会保存历史记录。

### 问题 4：端口被占用
```
错误: Address already in use
```

**解决：**
```bash
# 查找占用端口的进程
netstat -ano | findstr :8000

# 结束进程
taskkill /PID <进程ID> /F
```

## 性能优化

### 1. 使用更快的模型
```python
MODEL_NAME = "deepseek-coder:1.3b"  # 更快但质量稍低
```

### 2. 启用 GPU
Ollama 会自动使用 GPU（如果可用）

### 3. 调整并发
Flask 默认单线程，生产环境建议使用 gunicorn：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 simple_server_ollama_with_db:app
```

## 日志说明

服务运行时会输出：
```
收到客服请求，问题长度: 123
开始推理（使用 Ollama）...
推理完成，耗时: 2.34 秒
响应长度: 456
```

## 相关文件

- `simple_server_ollama_with_db.py` - 主服务程序
- `start_server_with_db_ollama.bat` - 原启动脚本
- `启动AI助手后端.bat` - 新启动脚本（本目录）
- `Ollama数据库版本说明.md` - 详细配置说明

## 与前端集成

前端通过以下方式调用：
```typescript
// 智能客服
fetch('http://localhost:8000/v1/assistant/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{ role: 'user', content: '用户问题' }]
  })
})

// 代码审计
fetch('http://localhost:8000/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [
      { role: 'system', content: '系统提示词' },
      { role: 'user', content: '代码内容' }
    ]
  })
})
```

## 总结

这个后端服务提供了两个主要功能：
1. **智能客服** - 快速回答用户问题
2. **代码审计** - 深度安全分析

使用 Ollama 本地推理，保护隐私，零成本运行！
