@echo off
chcp 65001 >nul
echo ========================================
echo 启动 Ollama + 数据库推理服务器
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

echo.
echo 安装必要的包...
pip install mysql-connector-python requests -q

echo.
echo 正在启动服务器...
echo 使用 Ollama 推理引擎（更快的推理速度）
echo 审计记录将自动保存到 MySQL 数据库
echo.
echo 请确保：
echo 1. Ollama 服务正在运行
echo 2. MySQL 服务正在运行
echo 3. 数据库 'rustsentinel' 已创建
echo.

python simple_server_ollama_with_db.py

pause
