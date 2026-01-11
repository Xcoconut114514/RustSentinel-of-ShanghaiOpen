@echo off
chcp 65001 >nul
echo ========================================
echo 启动 RustSentinel AI 助手后端服务
echo ========================================
echo.

REM 检查 Ollama 是否运行
echo 检查 Ollama 服务...
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama 未运行，请先启动 Ollama
    echo    下载地址: https://ollama.com/download
    echo.
    echo 启动 Ollama 后，请确保已下载模型：
    echo    ollama pull deepseek-coder:6.7b
    echo.
    pause
    exit /b 1
)
echo ✅ Ollama 服务正常
echo.

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate

echo.
echo 安装必要的包...
pip install mysql-connector-python requests flask flask-cors -q

echo.
echo ========================================
echo 正在启动 AI 助手后端服务...
echo ========================================
echo.
echo 服务功能：
echo 1. 代码审计 API: /v1/chat/completions
echo 2. 智能客服 API: /v1/assistant/chat
echo 3. 审计历史 API: /api/history
echo 4. 健康检查 API: /health
echo.
echo 使用 Ollama 推理引擎（更快的推理速度）
echo 审计记录将自动保存到 MySQL 数据库（如果配置）
echo.
echo 请确保：
echo 1. Ollama 服务正在运行
echo 2. MySQL 服务正在运行（可选）
echo 3. 数据库 'rustsentinel' 已创建（可选）
echo.
echo 服务地址: http://localhost:8000
echo.

python simple_server_ollama_with_db.py

pause
