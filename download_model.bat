@echo off
REM 使用国内镜像下载模型
echo ========================================
echo 使用 HuggingFace 国内镜像下载模型
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

REM 设置国内镜像
set HF_ENDPOINT=https://hf-mirror.com

REM 下载模型（会自动断点续传）
echo 开始下载模型...
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-7B --local-dir ./models/deepseek-r1

echo.
echo ========================================
echo 下载完成！
echo 模型保存位置: ./models/deepseek-r1
echo ========================================
pause
