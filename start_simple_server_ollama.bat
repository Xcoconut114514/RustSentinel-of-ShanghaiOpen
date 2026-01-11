@echo off
chcp 65001 >nul
echo ========================================
echo 启动 Ollama 推理服务器
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

echo.
echo 检查 Ollama 服务状态...
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Ollama 服务未运行
    echo 正在启动 Ollama...
    start "" ollama serve
    timeout /t 3 >nul
) else (
    echo ✅ Ollama 服务正常运行
)

echo.
echo 安装必要的包...
pip install flask flask-cors requests -q

echo.
echo 正在启动服务器...
echo 使用 Ollama 推理引擎
echo 预计推理时间：1-2 分钟
echo.

python simple_server_ollama.py

pause
