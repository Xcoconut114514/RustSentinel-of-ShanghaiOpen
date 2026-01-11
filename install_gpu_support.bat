@echo off
chcp 65001 >nul
echo ========================================
echo 安装 GPU 支持（CUDA 版本 PyTorch）
echo ========================================

echo.
echo 激活虚拟环境...
call venv\Scripts\activate

echo.
echo 检查当前 GPU 配置...
python check_gpu.py

echo.
echo ========================================
echo 是否需要安装 CUDA 版本的 PyTorch？
echo ========================================
echo.
echo 如果上面显示 "CUDA 不可用"，请按任意键继续安装
echo 如果显示 "CUDA 可用"，请直接关闭窗口
echo.
pause

echo.
echo ========================================
echo 开始安装 CUDA 版本的 PyTorch...
echo 这可能需要几分钟时间
echo ========================================
echo.

REM 卸载旧版本
echo 1. 卸载旧版本 PyTorch...
pip uninstall torch torchvision torchaudio -y

echo.
echo 2. 安装 CUDA 11.8 版本的 PyTorch...
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo ========================================
echo 安装完成！验证 GPU 配置...
echo ========================================
python check_gpu.py

echo.
echo ========================================
echo 如果看到 "CUDA 可用"，说明安装成功！
echo 现在可以重新启动后端服务了
echo ========================================
echo.

pause
