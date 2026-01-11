@echo off
chcp 65001 >nul
echo ========================================
echo 安装 CUDA 版本的 PyTorch
echo ========================================

echo.
echo 激活虚拟环境...
call venv\Scripts\activate

echo.
echo 1. 卸载当前的 CPU 版本...
pip uninstall torch torchvision torchaudio -y

echo.
echo 2. 安装 CUDA 11.8 版本（从官方源）...
echo 注意：必须使用官方源，国内镜像只有 CPU 版本！
echo.

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo ========================================
echo 安装完成！验证配置...
echo ========================================
echo.

python check_gpu.py

echo.
echo ========================================
echo 检查结果：
echo - 如果看到 "CUDA 可用" → 成功！
echo - 如果仍然是 "CPU 版本" → 请检查网络连接
echo ========================================
echo.

pause
