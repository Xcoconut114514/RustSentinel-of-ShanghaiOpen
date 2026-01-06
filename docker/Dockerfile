# RustSentinel Dockerfile
# 基于 Python 3.10 和 CUDA 支持

FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建符号链接
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# 升级 pip
RUN pip install --no-cache-dir --upgrade pip

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/models/deepseek-r1-distill
ENV VLLM_PORT=8000
ENV WEB_PORT=8501

# 暴露端口
EXPOSE 8000 8501

# 创建启动脚本
RUN echo '#!/bin/bash\n\
echo "启动 RustSentinel..."\n\
echo "正在启动 vLLM 推理服务..."\n\
vllm serve ${MODEL_PATH} \
    --dtype bfloat16 \
    --port ${VLLM_PORT} \
    --gpu-memory-utilization 0.9 \
    --model-name deepseek-audit &\n\
\n\
echo "等待 vLLM 服务启动..."\n\
sleep 30\n\
\n\
echo "启动 Web 界面..."\n\
cd /app/src\n\
python app_gradio.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# 启动命令
CMD ["/app/start.sh"]
