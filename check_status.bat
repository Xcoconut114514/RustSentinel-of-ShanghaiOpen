@echo off
chcp 65001 >nul
echo ========================================
echo 检查后端服务状态
echo ========================================
echo.

echo 1. 检查服务是否运行...
curl -s http://localhost:8000/health
echo.
echo.

echo 2. 检查端口占用...
netstat -ano | findstr :8000
echo.

echo 3. 检查 Python 进程...
tasklist | findstr python.exe
echo.

echo ========================================
echo 提示：
echo - 如果看到 {"status":"ok"} 说明服务正常
echo - 如果推理时间过长，可能是：
echo   1) 模型在 CPU 上运行（很慢）
echo   2) 代码太长，生成时间久
echo   3) 首次推理需要预热
echo ========================================
pause
