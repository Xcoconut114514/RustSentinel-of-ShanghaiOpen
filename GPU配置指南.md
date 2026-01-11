# GPU 推理配置指南

## 🎯 目标

将推理从 CPU 切换到 GPU，速度提升 10-50 倍！

## 📋 前置要求

1. ✅ NVIDIA GPU（你有 GeForce GPU）
2. ✅ 已安装 NVIDIA 驱动
3. ❓ 需要安装 CUDA 版本的 PyTorch

## 🚀 快速配置（3 步）

### 第 1 步：检查当前配置

```bash
cd httpsgithub.comXcoconut114514RustSentinel-of-ShanghaiOpen
venv\Scripts\activate
python check_gpu.py
```

**查看输出**:
- ✅ 如果显示 "CUDA 可用" → 跳到第 3 步
- ❌ 如果显示 "CUDA 不可用" → 继续第 2 步

### 第 2 步：安装 CUDA 版本的 PyTorch

#### 方法 A：使用自动安装脚本（推荐）

```bash
install_gpu_support.bat
```

这个脚本会：
1. 检查当前配置
2. 卸载 CPU 版本的 PyTorch
3. 安装 CUDA 11.8 版本的 PyTorch
4. 验证安装

#### 方法 B：手动安装

```bash
# 激活虚拟环境
venv\Scripts\activate

# 卸载旧版本
pip uninstall torch torchvision torchaudio -y

# 安装 CUDA 11.8 版本（推荐）
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 或者 CUDA 12.1 版本
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu128
#### 方法 C：使用国内镜像（如果官方源太慢）

```bash
pip3 install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 第 3 步：重启后端服务

```bash
# 停止当前服务（Ctrl+C）
# 然后重新启动
start_simple_server.bat
```

**查看启动日志**，应该看到类似：
```
正在加载模型...
Loading checkpoint shards: 100%
模型加载完成！
```

如果使用 GPU，加载速度会更快。

## 🔍 验证 GPU 是否在使用

### 方法 1：查看任务管理器

1. 打开任务管理器（Ctrl+Shift+Esc）
2. 切换到"性能"标签
3. 选择 GPU
4. 开始审计时，GPU 使用率应该飙升到 80-100%

### 方法 2：使用 nvidia-smi

```bash
# 打开新的命令行窗口
nvidia-smi

# 或者持续监控
nvidia-smi -l 1
```

应该看到 Python 进程占用 GPU 显存。

### 方法 3：查看后端日志

后端启动时会显示设备信息，如果使用 GPU 会看到：
```
device_map="auto"  # 自动选择设备
cuda:0             # 使用 GPU 0
```

## 📊 性能对比

### 你的代码（15 行）

| 推理方式 | 首次推理 | 后续推理 | GPU 使用率 |
|---------|---------|---------|-----------|
| CPU     | 10-20分钟 | 5-10分钟 | 0% |
| GPU     | 20-40秒  | 10-20秒  | 80-100% |

**速度提升**: 约 20-30 倍！

## 🐛 常见问题

### Q1: 安装后仍然显示 "CUDA 不可用"

**可能原因**:
1. NVIDIA 驱动版本太旧
2. CUDA 版本不匹配
3. 需要重启电脑

**解决方法**:
```bash
# 检查 NVIDIA 驱动版本
nvidia-smi

# 更新驱动（如果版本 < 450）
# 访问 https://www.nvidia.com/Download/index.aspx
```

### Q2: 安装过程中出现错误

**解决方法**:
```bash
# 清理缓存
pip cache purge

# 使用国内镜像
pip3 install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: GPU 显存不足

**错误信息**: `CUDA out of memory`

**解决方法**:
1. 关闭其他占用 GPU 的程序
2. 减少 batch size
3. 使用量化模型（8-bit）

### Q4: 安装的 PyTorch 版本不对

**检查版本**:
```python
import torch
print(torch.__version__)
# 应该看到类似: 2.x.x+cu118 或 2.x.x+cu121
# 如果只是 2.x.x（没有 +cu），说明是 CPU 版本
```

## 🔧 高级配置

### 使用 8-bit 量化（节省显存）

如果 GPU 显存不够，可以使用量化：

```bash
pip install bitsandbytes accelerate
```

然后修改 `simple_server.py`（如果需要）:
```python
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    load_in_8bit=True,  # 8-bit 量化
    device_map="auto",
    trust_remote_code=True
)
```

### 指定特定 GPU

如果有多个 GPU：

```bash
# 使用 GPU 0
set CUDA_VISIBLE_DEVICES=0
python simple_server.py

# 使用 GPU 1
set CUDA_VISIBLE_DEVICES=1
python simple_server.py
```

## 📝 完整流程示例

```bash
# 1. 进入项目目录
cd httpsgithub.comXcoconut114514RustSentinel-of-ShanghaiOpen

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 检查 GPU
python check_gpu.py

# 4. 如果 CUDA 不可用，安装 GPU 支持
install_gpu_support.bat

# 5. 再次检查
python check_gpu.py

# 6. 启动服务
start_simple_server.bat

# 7. 在前端测试
# 打开 http://localhost:3000
# 粘贴代码，点击审计
# 应该在 20-40 秒内得到结果
```

## 🎯 预期结果

### 安装前（CPU）:
```
CPU 使用率: 88%
GPU 使用率: 8%
推理时间: 10-20 分钟
```

### 安装后（GPU）:
```
CPU 使用率: 20-30%
GPU 使用率: 80-100%
推理时间: 20-40 秒
```

## 📞 需要帮助？

如果遇到问题，请提供：

1. `check_gpu.py` 的输出
2. `nvidia-smi` 的输出
3. 后端启动日志
4. 错误信息截图

## 🔗 相关资源

- [PyTorch 官方安装指南](https://pytorch.org/get-started/locally/)
- [CUDA 下载](https://developer.nvidia.com/cuda-downloads)
- [NVIDIA 驱动下载](https://www.nvidia.com/Download/index.aspx)

---

**总结**: 运行 `install_gpu_support.bat`，然后重启后端服务，推理速度将提升 20-30 倍！
