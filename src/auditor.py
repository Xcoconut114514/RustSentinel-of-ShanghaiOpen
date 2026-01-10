import os
from openai import OpenAI

# 读取刚才生成的 Rust 代码
with open("vulnerable_bank.rs", "r") as f:
    code = f.read()

# 连接刚才你启动的 C500 本地大模型
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

print(">>> 正在连接 C500 算力卡进行深度推理...")

response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[
        {"role": "system", "content": "你是一个资深的 Solana 智能合约安全审计专家。请仔细分析代码逻辑。如果发现‘权限绕过’或‘资金被盗’风险，请输出：1. [风险等级] 2. [攻击原理] 3. [修复代码]。"},
        {"role": "user", "content": f"请审计这段 Rust 代码，找出其中的致命漏洞:\n\n{code}"}
    ],
    temperature=0.1,
    max_tokens=1024
)

print("\n" + "="*15 + " AI 审计报告 " + "="*15)
print(response.choices[0].message.content)
