@echo off
REM 使用 ModelScope 下载模型（国内最快）
echo ========================================
echo 使用 ModelScope 下载模型（国内最快）
echo ========================================

REM 激活虚拟环境
call venv\Scripts\activate

REM 安装 ModelScope
echo 安装 ModelScope...
pip install modelscope -q

REM 下载模型
echo 开始下载模型...
python -c "from modelscope import snapshot_download; snapshot_download('deepseek-ai/DeepSeek-R1-Distill-Qwen-7B', cache_dir='./models')"

echo.
echo ========================================
echo 下载完成！
echo 模型保存位置: ./models
echo ========================================
pause
