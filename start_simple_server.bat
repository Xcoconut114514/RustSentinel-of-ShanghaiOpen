@echo off
chcp 65001 >nul
echo ========================================
echo 启动简易推理服务器
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

echo.
echo 安装必要的包...
pip install flask flask-cors transformers accelerate -q

echo.
echo 正在启动服务器...
echo 这可能需要 1-2 分钟加载模型到 GPU
echo.

python simple_server.py

pause
