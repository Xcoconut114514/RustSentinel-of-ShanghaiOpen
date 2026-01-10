"""
简单的本地推理服务器
使用 Transformers 直接加载模型，提供 OpenAI 兼容的 API
"""
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

print("正在加载模型...")
model_path = "./model/deepseek-r1"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True
)
print("模型加载完成！")

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    messages = data.get('messages', [])
    
    # 构建提示词
    prompt = ""
    for msg in messages:
        role = msg['role']
        content = msg['content']
        if role == 'system':
            prompt += f"System: {content}\n\n"
        elif role == 'user':
            prompt += f"User: {content}\n\nAssistant: "
    
    # 生成回复
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=2048,
        temperature=0.2,
        do_sample=True,
        top_p=0.95
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 提取助手回复
    assistant_response = response.split("Assistant:")[-1].strip()
    
    return jsonify({
        "choices": [{
            "message": {
                "role": "assistant",
                "content": assistant_response
            }
        }]
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("服务器启动成功！")
    print("API 地址: http://localhost:8000/v1/chat/completions")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=8000, debug=False)
