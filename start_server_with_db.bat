@echo off
chcp 65001 >nul
echo ========================================
echo 启动带数据库支持的推理服务器
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

echo.
echo 安装必要的包...
pip install mysql-connector-python -q

echo.
echo 正在启动服务器...
echo 审计记录将自动保存到 MySQL 数据库
echo.

python simple_server_with_db.py

pause
