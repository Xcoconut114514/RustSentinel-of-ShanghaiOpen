@echo off
chcp 65001 >nul
echo ========================================
echo 修复 CORS 问题
echo ========================================

echo.
echo 激活虚拟环境...
call venv\Scripts\activate

echo.
echo 安装 flask-cors...
pip install flask-cors

echo.
echo ========================================
echo 修复完成！
echo 请重新运行 start_simple_server.bat
echo ========================================
echo.

pause
