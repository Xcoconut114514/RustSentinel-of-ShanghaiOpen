# Docker 部署指南

本文档介绍如何使用 Docker 部署 RustSentinel。

## 前置要求

### 软件要求

- Docker 20.10 或更高版本
- Docker Compose 1.29 或更高版本（可选）
- NVIDIA Container Toolkit（GPU 支持）

### 硬件要求

- NVIDIA GPU（支持 CUDA 11.8+）
- 至少 24GB GPU 显存
- 32GB 系统内存
- 100GB 可用磁盘空间

## 安装 Docker 和 NVIDIA Container Toolkit

### Ubuntu/Debian

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 重启 Docker
sudo systemctl restart docker
```

### CentOS/RHEL

```bash
# 安装 Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | \
    sudo tee /etc/yum.repos.d/nvidia-docker.repo

sudo yum install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 验证安装

```bash
# 测试 Docker
docker run hello-world

# 测试 GPU 支持
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

## 构建镜像

### 方法 1: 从源码构建

```bash
# 克隆仓库
git clone https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen.git
cd RustSentinel-of-ShanghaiOpen

# 构建镜像
docker build -t rustsentinel:latest -f docker/Dockerfile .

# 查看镜像
docker images | grep rustsentinel
```

### 方法 2: 使用 Docker Hub（计划中）

```bash
# 拉取预构建镜像
docker pull xcoconut114514/rustsentinel:latest
```

## 运行容器

### 基础运行

```bash
docker run -d \
    --name rustsentinel \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    rustsentinel:latest
```

### 挂载数据卷

```bash
# 创建数据目录
mkdir -p ~/rustsentinel/{models,config,logs}

# 运行容器并挂载数据卷
docker run -d \
    --name rustsentinel \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    -v ~/rustsentinel/models:/app/models \
    -v ~/rustsentinel/config:/app/config \
    -v ~/rustsentinel/logs:/app/logs \
    rustsentinel:latest
```

### 环境变量配置

```bash
docker run -d \
    --name rustsentinel \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    -e MODEL_PATH=/app/models/deepseek-r1-distill \
    -e GPU_MEMORY_UTILIZATION=0.9 \
    -e LOG_LEVEL=INFO \
    rustsentinel:latest
```

## 使用 Docker Compose

### 1. 准备配置文件

编辑 `docker/docker-compose.yml`（已提供）。

### 2. 启动服务

```bash
# 在项目根目录
docker-compose -f docker/docker-compose.yml up -d

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f

# 停止服务
docker-compose -f docker/docker-compose.yml down
```

## 容器管理

### 查看容器状态

```bash
# 列出所有容器
docker ps -a

# 查看容器日志
docker logs rustsentinel

# 实时查看日志
docker logs -f rustsentinel

# 查看最近 100 行日志
docker logs --tail 100 rustsentinel
```

### 进入容器

```bash
# 进入容器 bash
docker exec -it rustsentinel bash

# 执行单个命令
docker exec rustsentinel nvidia-smi
```

### 停止和重启

```bash
# 停止容器
docker stop rustsentinel

# 启动容器
docker start rustsentinel

# 重启容器
docker restart rustsentinel
```

### 删除容器

```bash
# 停止并删除容器
docker stop rustsentinel
docker rm rustsentinel

# 强制删除运行中的容器
docker rm -f rustsentinel
```

## 数据持久化

### 模型文件

将模型文件放在主机的 `~/rustsentinel/models/` 目录：

```bash
# 下载模型到主机
cd ~/rustsentinel/models
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-7B

# 容器会自动使用这个目录的模型
```

### 配置文件

自定义配置放在 `~/rustsentinel/config/`：

```bash
# 创建自定义系统提示词
cat > ~/rustsentinel/config/custom_prompt.txt << 'EOF'
你是一个专业的智能合约安全审计专家...
EOF
```

### 日志文件

日志会自动保存到 `~/rustsentinel/logs/`：

```bash
# 查看日志
tail -f ~/rustsentinel/logs/app.log
```

## 网络配置

### 端口映射

默认端口映射：
- `8000`: vLLM API 服务
- `8501`: Gradio Web 界面

修改端口映射：

```bash
docker run -d \
    --name rustsentinel \
    --gpus all \
    -p 9000:8000 \  # 将 vLLM 映射到主机 9000 端口
    -p 9501:8501 \  # 将 Web 界面映射到主机 9501 端口
    rustsentinel:latest
```

### 网络隔离

创建独立网络：

```bash
# 创建网络
docker network create rustsentinel-net

# 在指定网络中运行
docker run -d \
    --name rustsentinel \
    --network rustsentinel-net \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    rustsentinel:latest
```

## 性能优化

### GPU 资源限制

```bash
# 使用特定 GPU
docker run -d \
    --name rustsentinel \
    --gpus '"device=0"' \  # 仅使用 GPU 0
    rustsentinel:latest

# 使用多个 GPU
docker run -d \
    --name rustsentinel \
    --gpus '"device=0,1"' \  # 使用 GPU 0 和 1
    rustsentinel:latest
```

### 内存限制

```bash
docker run -d \
    --name rustsentinel \
    --gpus all \
    --memory=32g \          # 限制系统内存为 32GB
    --memory-swap=64g \     # 限制 swap 为 64GB
    rustsentinel:latest
```

### CPU 限制

```bash
docker run -d \
    --name rustsentinel \
    --gpus all \
    --cpus=8 \              # 限制使用 8 个 CPU 核心
    rustsentinel:latest
```

## 故障排除

### 容器无法启动

```bash
# 查看详细错误信息
docker logs rustsentinel

# 检查容器配置
docker inspect rustsentinel
```

### GPU 不可用

```bash
# 验证 NVIDIA Runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# 检查 Docker 守护进程配置
cat /etc/docker/daemon.json
```

### 端口冲突

```bash
# 查看端口占用
sudo netstat -tuln | grep -E "8000|8501"

# 使用不同端口
docker run -d \
    --name rustsentinel \
    --gpus all \
    -p 9000:8000 \
    -p 9501:8501 \
    rustsentinel:latest
```

### 显存不足

编辑环境变量：

```bash
docker run -d \
    --name rustsentinel \
    --gpus all \
    -e GPU_MEMORY_UTILIZATION=0.7 \  # 降低显存利用率
    rustsentinel:latest
```

## 生产环境部署

### 使用 Docker Swarm

```bash
# 初始化 Swarm
docker swarm init

# 部署服务
docker stack deploy -c docker/docker-compose.yml rustsentinel

# 查看服务
docker service ls
```

### 使用 Kubernetes

参考 `docker/k8s-deployment.yaml`（计划中）。

## 安全建议

1. **不要暴露端口到公网**：仅在内网使用或通过 VPN 访问
2. **使用非 root 用户**：修改 Dockerfile 添加普通用户
3. **启用认证**：配置 Gradio 用户名和密码
4. **定期更新镜像**：修复安全漏洞
5. **限制资源使用**：防止资源耗尽

## 更新和维护

### 更新镜像

```bash
# 拉取最新代码
cd RustSentinel-of-ShanghaiOpen
git pull

# 重新构建镜像
docker build -t rustsentinel:latest -f docker/Dockerfile .

# 停止旧容器
docker stop rustsentinel
docker rm rustsentinel

# 启动新容器
docker run -d \
    --name rustsentinel \
    --gpus all \
    -p 8000:8000 \
    -p 8501:8501 \
    -v ~/rustsentinel/models:/app/models \
    rustsentinel:latest
```

### 备份数据

```bash
# 备份模型和配置
tar -czf rustsentinel-backup-$(date +%Y%m%d).tar.gz ~/rustsentinel/
```

---

更多信息请参考 [主文档](../README.md) 和 [部署文档](deployment.md)。
