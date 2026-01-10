#!/bin/bash

# RustSentinel 快速启动脚本
# 此脚本帮助您快速搭建 RustSentinel 环境

set -e  # 遇到错误立即退出

echo "================================================"
echo "  RustSentinel 快速部署脚本"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python 版本
echo -e "${YELLOW}[1/6] 检查 Python 版本...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 python3，请先安装 Python 3.10+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ 找到 Python $PYTHON_VERSION${NC}"

# 创建虚拟环境
echo -e "\n${YELLOW}[2/6] 创建 Python 虚拟环境...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}虚拟环境已存在，跳过创建${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
fi

# 激活虚拟环境
echo -e "\n${YELLOW}[3/6] 激活虚拟环境...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ 虚拟环境已激活${NC}"

# 安装依赖
echo -e "\n${YELLOW}[4/6] 安装依赖包...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt
echo -e "${GREEN}✓ 依赖安装完成${NC}"

# 创建配置文件
echo -e "\n${YELLOW}[5/6] 创建配置文件...${NC}"
if [ ! -f "config/.env" ]; then
    cp config/example.env config/.env
    echo -e "${GREEN}✓ 配置文件已创建: config/.env${NC}"
    echo -e "${YELLOW}提示: 请根据需要编辑 config/.env${NC}"
else
    echo -e "${YELLOW}配置文件已存在，跳过创建${NC}"
fi

# 检查 GPU
echo -e "\n${YELLOW}[6/6] 检查 GPU 环境...${NC}"
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✓ 检测到 NVIDIA GPU${NC}"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo -e "${YELLOW}⚠ 未检测到 NVIDIA GPU${NC}"
    echo -e "${YELLOW}  本项目需要 GPU 才能运行推理服务${NC}"
fi

echo ""
echo "================================================"
echo -e "${GREEN}✓ 环境配置完成！${NC}"
echo "================================================"
echo ""
echo "接下来的步骤："
echo ""
echo "1. 下载模型文件："
echo "   huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
echo ""
echo "2. 启动 vLLM 服务（终端 1）："
echo "   vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \\"
echo "       --dtype bfloat16 \\"
echo "       --port 8000 \\"
echo "       --model-name deepseek-audit"
echo ""
echo "3. 启动 Web 界面（终端 2）："
echo "   python src/app_gradio.py"
echo ""
echo "4. 访问界面："
echo "   http://localhost:8501"
echo ""
echo "详细文档请查看: README.md 或 docs/deployment.md"
echo ""
