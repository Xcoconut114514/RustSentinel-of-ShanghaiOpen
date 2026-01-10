# 部署说明文档

## 📋 最低系统要求

### 硬件要求

#### 推荐配置（生产环境）
- **GPU**: 沐曦 C500 (64GB 显存) 或 NVIDIA A100/H100
- **CPU**: 16 核心或以上
- **内存**: 64GB RAM 或以上
- **存储**: 200GB 可用空间（SSD 推荐）
- **网络**: 内网环境即可（支持完全离线部署）

#### 最低配置（测试/开发环境）
- **GPU**: NVIDIA RTX 3090 (24GB 显存) 或同等算力
- **CPU**: 8 核心
- **内存**: 32GB RAM
- **存储**: 100GB 可用空间
- **网络**: 内网环境即可

### 软件要求

- **操作系统**: 
  - Ubuntu 20.04 LTS 或更高版本（推荐）
  - CentOS 8 或更高版本
  - Windows 10/11 with WSL2（部分功能受限）
  
- **Python**: 3.10, 3.11, 3.12
  
- **CUDA**: 11.8 或更高版本（NVIDIA GPU）
  
- **Docker**: 20.10 或更高版本（可选，用于容器化部署）

## 🚀 一步步部署指南

### 方案一：标准部署（推荐）

#### 步骤 1: 系统环境准备

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y git wget curl build-essential

# 安装 Python 3.10+
sudo apt install -y python3.10 python3.10-venv python3-pip

# 验证安装
python3 --version  # 应显示 Python 3.10.x 或更高
```

#### 步骤 2: 克隆项目仓库

```bash
# 克隆仓库到本地
git clone https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen.git

# 进入项目目录
cd RustSentinel-of-ShanghaiOpen
```

#### 步骤 3: 创建虚拟环境

```bash
# 创建 Python 虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate   # Windows
```

#### 步骤 4: 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 验证安装
pip list | grep -E "openai|gradio|vllm"
```

#### 步骤 5: 下载模型文件

**方法 A: 使用 HuggingFace（国外用户）**

```bash
# 安装 HuggingFace CLI
pip install -U huggingface_hub

# 登录（可选，公开模型不需要）
huggingface-cli login

# 下载模型
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --local-dir ./models/deepseek-r1-distill
```

**方法 B: 使用 ModelScope（国内推荐）**

```bash
# 安装 ModelScope
pip install modelscope

# 下载模型
python -c "
from modelscope import snapshot_download
model_dir = snapshot_download(
    'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
    cache_dir='./models'
)
print(f'模型已下载到: {model_dir}')
"
```

**方法 C: 手动下载**

1. 访问 [DeepSeek-R1 模型页面](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)
2. 下载所有模型文件到 `./models/deepseek-r1-distill/` 目录
3. 确保目录结构如下：
   ```
   models/
   └── deepseek-r1-distill/
       ├── config.json
       ├── tokenizer.json
       ├── model.safetensors
       └── ...
   ```

#### 步骤 6: 配置环境变量

```bash
# 创建配置文件
cp config/example.env config/.env

# 编辑配置文件
nano config/.env
```

在 `.env` 文件中设置：

```bash
# 模型路径
MODEL_PATH=./models/deepseek-r1-distill

# vLLM 服务配置
VLLM_HOST=0.0.0.0
VLLM_PORT=8000

# Web 界面配置
WEB_HOST=0.0.0.0
WEB_PORT=8501

# GPU 配置
GPU_MEMORY_UTILIZATION=0.9
TENSOR_PARALLEL_SIZE=1
```

#### 步骤 7: 启动推理引擎

在第一个终端窗口中启动 vLLM 服务：

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 vLLM（基础配置）
vllm serve ./models/deepseek-r1-distill \
    --dtype bfloat16 \
    --port 8000 \
    --gpu-memory-utilization 0.9 \
    --model-name deepseek-audit

# 或使用完整配置
vllm serve ./models/deepseek-r1-distill \
    --dtype bfloat16 \
    --port 8000 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.9 \
    --model-name deepseek-audit \
    --max-model-len 8192 \
    --trust-remote-code
```

等待看到以下输出表示启动成功：
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 步骤 8: 启动 Web 界面

在第二个终端窗口中启动 Gradio 界面：

```bash
# 激活虚拟环境
source venv/bin/activate

# 进入源码目录
cd src

# 启动 Gradio 应用
python app_gradio.py
```

成功启动后，访问：
- **本地访问**: http://localhost:8501
- **局域网访问**: http://YOUR_IP:8501

### 方案二：Docker 部署

#### 步骤 1: 安装 Docker 和 NVIDIA Container Toolkit

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

#### 步骤 2: 构建 Docker 镜像

```bash
# 克隆仓库
git clone https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen.git
cd RustSentinel-of-ShanghaiOpen

# 构建镜像
docker build -t rustsentinel:latest -f docker/Dockerfile .
```

#### 步骤 3: 运行容器

```bash
# 运行容器（前台）
docker run --rm \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    -v $(pwd)/models:/app/models \
    rustsentinel:latest

# 或后台运行
docker run -d \
    --name rustsentinel \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    -v $(pwd)/models:/app/models \
    --restart unless-stopped \
    rustsentinel:latest

# 查看日志
docker logs -f rustsentinel
```

### 方案三：生产环境部署（Kubernetes）

详细配置请参考 [docker/k8s-deployment.yaml](../docker/k8s-deployment.yaml)

## 🔧 环境变量配置

### 必需配置

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `MODEL_PATH` | 模型文件路径 | `./models/deepseek-r1-distill` | `/data/models/deepseek` |
| `VLLM_PORT` | vLLM 服务端口 | `8000` | `8000` |
| `WEB_PORT` | Web 界面端口 | `8501` | `8501` |

### 可选配置

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `GPU_MEMORY_UTILIZATION` | GPU 显存利用率 | `0.9` | `0.8` |
| `MAX_MODEL_LEN` | 最大上下文长度 | `8192` | `16384` |
| `TENSOR_PARALLEL_SIZE` | 张量并行数 | `1` | `2` |
| `DTYPE` | 数据类型 | `bfloat16` | `float16` |

### 高级配置

```bash
# 启用量化（减少显存占用）
QUANTIZATION=awq

# 启用 Flash Attention 2（加速推理）
ENABLE_FLASH_ATTN=true

# 自定义系统提示词路径
SYSTEM_PROMPT_PATH=./config/custom_prompt.txt

# 日志级别
LOG_LEVEL=INFO
```

## ❓ 常见问题解答 (FAQ)

### Q1: 启动 vLLM 时提示显存不足怎么办？

**A**: 尝试以下解决方案：

1. **降低显存利用率**:
   ```bash
   vllm serve ... --gpu-memory-utilization 0.7
   ```

2. **使用量化模型**:
   ```bash
   vllm serve ... --quantization awq
   ```

3. **减少最大序列长度**:
   ```bash
   vllm serve ... --max-model-len 4096
   ```

4. **使用多 GPU 并行**:
   ```bash
   vllm serve ... --tensor-parallel-size 2
   ```

### Q2: Web 界面无法访问怎么办？

**A**: 检查以下事项：

1. **确认服务已启动**:
   ```bash
   ps aux | grep "app_gradio"
   netstat -tuln | grep 8501
   ```

2. **检查防火墙规则**:
   ```bash
   sudo ufw allow 8501/tcp
   ```

3. **修改监听地址**:
   在 `src/app_gradio.py` 中确保：
   ```python
   demo.launch(server_name="0.0.0.0", server_port=8501)
   ```

### Q3: 模型下载速度慢或失败？

**A**: 使用国内镜像：

```bash
# 设置 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com

# 或使用 ModelScope
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('deepseek-ai/DeepSeek-R1-Distill-Qwen-7B')"
```

### Q4: 如何在没有 GPU 的环境下运行？

**A**: 不推荐 CPU 部署（速度极慢），但可以：

```bash
# 使用 CPU 模式（仅用于测试）
vllm serve ./models/deepseek-r1-distill \
    --device cpu \
    --dtype float32
```

或考虑使用云端 GPU 服务。

### Q5: 如何更新到最新版本？

**A**: 执行以下命令：

```bash
cd RustSentinel-of-ShanghaiOpen
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Q6: 可以同时审计多个文件吗？

**A**: 当前版本主要支持单文件审计。批量审计功能正在开发中，您可以：

1. 编写脚本循环调用 API
2. 使用 `examples/batch_audit.py`（即将推出）
3. 关注项目更新

### Q7: 如何自定义审计规则？

**A**: 修改系统提示词：

1. 编辑 `config/system_prompt.txt`
2. 添加自定义检测规则，例如：
   ```
   重点检测以下漏洞类型：
   1. Signer 检查缺失
   2. 账户所有权验证缺失
   3. 整数溢出/下溢
   4. 重入攻击
   5. [你的自定义规则]
   ```
3. 重启服务生效

### Q8: 部署在云服务器上，如何保证安全？

**A**: 建议措施：

1. **使用 VPN/SSH 隧道**:
   ```bash
   ssh -L 8501:localhost:8501 user@server
   ```

2. **启用身份验证**（在 Gradio 中）:
   ```python
   demo.launch(auth=("admin", "your_password"))
   ```

3. **配置防火墙**，仅允许内网访问

4. **使用 HTTPS**（配合 Nginx 反向代理）

### Q9: 如何查看详细日志？

**A**: 启用调试模式：

```bash
# 启动 vLLM 时
vllm serve ... --log-level DEBUG

# 启动 Gradio 时
LOG_LEVEL=DEBUG python src/app_gradio.py
```

### Q10: 支持哪些 Rust 框架的审计？

**A**: 当前主要支持：

- ✅ Anchor Framework (Solana)
- ✅ 原生 Solana 程序
- 🚧 Substrate (计划中)
- 🚧 Move (计划中)

## 🔗 相关链接

- [主文档](../README.md)
- [技术架构](architecture.md)
- [使用示例](../examples/)
- [问题反馈](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues)

---

如有其他问题，请联系技术支持：2819404727@qq.com
