@echo off
chcp 65001 >nul
echo ========================================
echo 切换到国内镜像，加速下载
echo ========================================
echo.
echo 请按 Ctrl+C 停止当前下载，然后：
echo.
echo 1. 关闭当前下载窗口
echo 2. 双击运行本脚本
echo.
echo ========================================
pause

REM 激活虚拟环境
call venv\Scripts\activate

REM 设置国内镜像
set HF_ENDPOINT=https://hf-mirror.com

echo.
echo 正在使用国内镜像下载...
echo 速度预计：5-10 MB/s
echo.

REM 下载模型
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-7B

echo.
echo ========================================
echo 下载完成！
echo ========================================
pause
