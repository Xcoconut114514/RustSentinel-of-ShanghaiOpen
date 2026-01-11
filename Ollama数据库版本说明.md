# Ollama + 数据库版本说明

## 概述

`start_server_with_db_ollama.bat` 结合了 Ollama 推理引擎和 MySQL 数据库支持，提供：
- ✅ 更快的推理速度（使用 Ollama）
- ✅ 更好的 GPU 支持
- ✅ 自动保存审计历史到数据库
- ✅ 完整的历史记录查询 API

## 前置要求

### 1. 安装 Ollama
```bash
# 下载并安装 Ollama for Windows
# https://ollama.com/download
```

### 2. 下载并运行模型
```bash
# 下载 DeepSeek Coder 模型
ollama pull deepseek-coder:6.7b

# 或者使用其他模型（需要修改配置）
ollama pull codellama:7b
```

### 3. 安装 MySQL
- 确保 MySQL 服务正在运行
- 创建数据库：
```sql
CREATE DATABASE rustsentinel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 配置数据库连接
编辑 `simple_server_ollama_with_db.py` 中的数据库配置：
```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',  # 修改为你的密码
    'database': 'rustsentinel',
    'port': 3306
}
```

## 使用方法

### 启动服务器
```bash
start_server_with_db_ollama.bat
```

### API 端点

#### 1. 代码审计
```
POST http://localhost:8000/v1/chat/completions
```

#### 2. 获取审计历史
```
GET http://localhost:8000/api/history?page=1&page_size=10
```

#### 3. 获取单条记录
```
GET http://localhost:8000/api/history/{id}
```

#### 4. 删除记录
```
DELETE http://localhost:8000/api/history/{id}
```

#### 5. 健康检查
```
GET http://localhost:8000/health
```

## 配置选项

### 修改模型
编辑 `simple_server_ollama_with_db.py`：
```python
MODEL_NAME = "deepseek-coder:6.7b"  # 改为其他模型
```

### 修改推理参数
```python
"options": {
    "temperature": 0.2,      # 温度（0-1）
    "num_predict": 2048      # 最大生成 token 数
}
```

### 修改输出语言
代码已配置为中文输出。如需修改为英文，编辑 `simple_server_ollama_with_db.py`：
```python
# 中文输出（当前配置）
prompt += "请用中文回答。分析以上 Rust 代码的安全问题，包括：风险等级、攻击原理、缓解措施等。\n\nAssistant: "

# 英文输出
prompt += "Assistant: "
```

## 优势对比

| 特性 | 原版 (GPU) | Ollama 版本 |
|------|-----------|------------|
| 推理速度 | 较慢 | 更快 |
| GPU 支持 | 需要配置 | 自动优化 |
| 内存占用 | 较高 | 较低 |
| 模型切换 | 困难 | 简单 |
| 数据库支持 | ✅ | ✅ |

## 故障排除

### Ollama 未运行
```bash
# 检查 Ollama 状态
ollama list

# 启动 Ollama 服务（通常自动启动）
# Windows: 从开始菜单启动 Ollama
```

### 数据库连接失败
1. 检查 MySQL 服务是否运行
2. 验证数据库配置（用户名、密码、数据库名）
3. 确保数据库 `rustsentinel` 已创建

### 模型未找到
```bash
# 查看已安装的模型
ollama list

# 下载所需模型
ollama pull deepseek-coder:6.7b
```

## 性能建议

1. **使用 GPU**：Ollama 会自动使用 GPU（如果可用）
2. **调整 batch size**：根据 GPU 内存调整
3. **选择合适的模型**：
   - `deepseek-coder:6.7b` - 平衡性能和质量
   - `codellama:7b` - 更快但质量稍低
   - `deepseek-coder:33b` - 最高质量但需要更多资源

## 与前端集成

前端无需修改，API 接口完全兼容原版。只需确保：
1. 后端服务运行在 `http://localhost:8000`
2. 前端配置的 API 地址正确

## 相关文件

- `simple_server_ollama_with_db.py` - 服务器主程序
- `start_server_with_db_ollama.bat` - 启动脚本
- `使用Ollama运行.md` - Ollama 基础使用说明
- `数据库功能说明.md` - 数据库功能详细说明
