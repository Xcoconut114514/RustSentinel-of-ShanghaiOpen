"""
检查 GPU 和 CUDA 配置
"""
import torch
import sys

print("=" * 50)
print("GPU 配置检查")
print("=" * 50)

# 检查 PyTorch 版本
print(f"\n1. PyTorch 版本: {torch.__version__}")

# 检查 CUDA 是否可用
print(f"\n2. CUDA 是否可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"   ✅ CUDA 可用！")
    print(f"   CUDA 版本: {torch.version.cuda}")
    print(f"   GPU 数量: {torch.cuda.device_count()}")
    
    for i in range(torch.cuda.device_count()):
        print(f"\n   GPU {i}:")
        print(f"   - 名称: {torch.cuda.get_device_name(i)}")
        print(f"   - 显存: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
else:
    print(f"   ❌ CUDA 不可用")
    print(f"\n   可能的原因:")
    print(f"   1. PyTorch 是 CPU 版本")
    print(f"   2. CUDA 驱动未安装")
    print(f"   3. GPU 驱动版本不兼容")

# 检查 cuDNN
print(f"\n3. cuDNN 版本: {torch.backends.cudnn.version() if torch.cuda.is_available() else 'N/A'}")

# 测试 GPU
if torch.cuda.is_available():
    print(f"\n4. 测试 GPU 计算:")
    try:
        x = torch.randn(100, 100).cuda()
        y = torch.randn(100, 100).cuda()
        z = torch.matmul(x, y)
        print(f"   ✅ GPU 计算正常！")
    except Exception as e:
        print(f"   ❌ GPU 计算失败: {e}")
else:
    print(f"\n4. 跳过 GPU 测试（CUDA 不可用）")

print("\n" + "=" * 50)
print("建议:")
print("=" * 50)

if not torch.cuda.is_available():
    print("\n需要安装支持 CUDA 的 PyTorch:")
    print("\n方法 1 (推荐 - CUDA 11.8):")
    print("pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print("\n方法 2 (CUDA 12.1):")
    print("pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print("\n方法 3 (使用国内镜像):")
    print("pip3 install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple")
else:
    print("\n✅ GPU 配置正常，可以使用 GPU 推理！")

print("\n" + "=" * 50)
