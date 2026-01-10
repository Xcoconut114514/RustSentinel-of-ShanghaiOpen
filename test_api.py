"""测试 API 是否正常工作"""
from openai import OpenAI

print("正在测试 API 连接...")

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

try:
    print("发送测试请求...")
    response = client.chat.completions.create(
        model="deepseek-audit",
        messages=[
            {"role": "system", "content": "你是一个助手"},
            {"role": "user", "content": "说'你好'"}
        ],
        temperature=0.2,
        max_tokens=50
    )
    
    print("\n✅ API 测试成功！")
    print(f"回复: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ API 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
