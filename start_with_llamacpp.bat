@echo off
chcp 65001 >nul
echo ========================================
echo 使用 llama.cpp 启动 RustSentinel
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

echo.
echo 安装 llama-cpp-python...
pip install llama-cpp-python[server] --upgrade

echo.
echo 启动模型服务器...
echo 注意：首次运行需要转换模型格式
echo.

python -m llama_cpp.server ^
    --model ./model/deepseek-r1 ^
    --host 0.0.0.0 ^
    --port 8000 ^
    --n_gpu_layers 35

pause
