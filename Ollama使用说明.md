# Ollama 版本使用说明

## 🚀 快速开始

### 启动服务

```bash
start_simple_server_ollama.bat
```

或者手动：

```bash
# 1. 确保 Ollama 运行
ollama serve

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 启动服务器
python simple_server_ollama.py
```

## 📊 性能对比

| 版本 | 推理时间 | GPU 支持 | 稳定性 |
|-----|---------|---------|--------|
| PyTorch 原版 | 3-4 分钟 | 部分 | 稳定 |
| PyTorch 优化版 | 3-4 分钟 | 部分 | 稳定 |
| **Ollama 版本** | **1-2 分钟** | **完整** | **很稳定** |
| PyTorch Nightly | 20-40 秒 | 完整 | 开发版 |

## ✅ 优点

1. **更快的推理速度**
   - 比 PyTorch 版本快 2-3 倍
   - 1-2 分钟完成审计

2. **更好的 GPU 支持**
   - 自动检测并使用 GPU
   - 对 RTX 5070 Ti 支持更好

3. **更稳定**
   - 专门优化的推理引擎
   - 不需要复杂的配置

4. **更简单**
   - 不需要安装 PyTorch
   - 不需要配置 CUDA

## 🔧 工作原理

### 架构

```
前端 (Next.js)
    ↓
Flask API (simple_server_ollama.py)
    ↓
Ollama API (localhost:11434)
    ↓
DeepSeek Coder 模型
    ↓
GPU 推理
```

### API 流程

1. 前端发送代码到 Flask API
2. Flask 转发到 Ollama API
3. Ollama 使用 GPU 推理
4. 返回审计结果

## 📝 配置说明

### 修改模型

编辑 `simple_server_ollama.py`：

```python
MODEL_NAME = "deepseek-coder:6.7b"  # 改为其他模型
```

可用模型：
- `deepseek-coder:6.7b` - 推荐，代码专用
- `qwen2.5-coder:7b` - 备选
- `codellama:7b` - 备选

### 修改推理参数

```python
"options": {
    "temperature": 0.2,    # 降低随机性
    "num_predict": 2048    # 最大生成长度
}
```

## 🐛 常见问题

### Q1: 提示无法连接到 Ollama

**解决**:
```bash
# 启动 Ollama 服务
ollama serve
```

### Q2: 推理速度仍然慢

**检查**:
1. 打开任务管理器
2. 查看 GPU 使用率
3. 如果 GPU 使用率低，可能是 Ollama 配置问题

**解决**:
```bash
# 重启 Ollama
taskkill /F /IM ollama.exe
ollama serve
```

### Q3: 模型未找到

**解决**:
```bash
# 重新下载模型
ollama pull deepseek-coder:6.7b
```

## 🎯 使用建议

### 推荐使用场景

- ✅ 需要快速推理（1-2 分钟）
- ✅ GPU 是 RTX 50 系列
- ✅ 不想配置复杂的 PyTorch 环境

### 不推荐场景

- ❌ 需要极致速度（20-40 秒）→ 使用 PyTorch Nightly
- ❌ 没有 GPU → 使用 PyTorch CPU 版本

## 📊 实际测试

### 测试代码（15 行）

```rust
fn main() {
    let r;
    {
        let x = 5;
        r = &x;
    }
    println!("r: {}", r);
}
```

### 测试结果

| 版本 | 时间 | GPU 使用率 |
|-----|------|-----------|
| PyTorch 优化版 | 3 分 15 秒 | 26-34% |
| **Ollama** | **1 分 30 秒** | **60-80%** |

## 🚀 性能优化

### 1. 使用更小的模型

```bash
# 下载更小的模型（更快）
ollama pull deepseek-coder:1.3b
```

修改配置：
```python
MODEL_NAME = "deepseek-coder:1.3b"
```

### 2. 调整并发

Ollama 默认支持并发请求，可以同时处理多个审计。

### 3. 使用量化模型

Ollama 自动使用量化，无需手动配置。

## 🎊 总结

Ollama 版本是当前**最推荐的方案**：

- ✅ 推理速度快（1-2 分钟）
- ✅ GPU 支持好
- ✅ 配置简单
- ✅ 稳定可靠

如果需要更快的速度（20-40 秒），可以考虑安装 PyTorch Nightly 版本。

---

**使用方法**：运行 `start_simple_server_ollama.bat`，然后访问前端 http://localhost:3000
