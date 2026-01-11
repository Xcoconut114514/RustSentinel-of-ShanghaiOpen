@echo off
chcp 65001 >nul
echo ========================================
echo 启动优化版推理服务器（8-bit 量化）
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

echo.
echo 检查并安装必要的包...
pip install bitsandbytes accelerate -q

echo.
echo 正在启动优化版服务器...
echo 使用 8-bit 量化，完全运行在 GPU 上
echo 预计推理时间：20-40 秒
echo.

python simple_server_optimized.py

pause
