"""检查推理服务器是否正常"""
import requests
import json

print("正在检查推理服务器...")
print("="*50)

# 测试健康检查端点
try:
    print("\n1. 测试健康检查端点...")
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 健康检查通过")
except Exception as e:
    print(f"   ❌ 健康检查失败: {e}")
    print("\n推理服务器可能没有运行！")
    print("请确保 simple_server.py 正在运行")
    exit(1)

# 测试 API 端点
try:
    print("\n2. 测试 API 端点...")
    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        json={
            "messages": [
                {"role": "system", "content": "你是一个助手"},
                {"role": "user", "content": "说'测试成功'"}
            ]
        },
        timeout=30
    )
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   回复: {result['choices'][0]['message']['content']}")
        print("   ✅ API 测试通过")
    else:
        print(f"   ❌ API 返回错误: {response.text}")
except Exception as e:
    print(f"   ❌ API 测试失败: {e}")

print("\n" + "="*50)
print("测试完成")
