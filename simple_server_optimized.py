"""
优化版本的推理服务器
使用 8-bit 量化，完全加载到 GPU，速度更快
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

app = Flask(__name__)
CORS(app)

print("正在加载模型（8-bit 量化版本）...")
print("这将显著减少显存占用，让模型完全运行在 GPU 上")

model_path = "./model/deepseek-r1"

# 配置 8-bit 量化
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False,
)

tokenizer = AutoTokenizer.from_pretrained(model_path)

print("加载模型到 GPU（8-bit 量化）...")
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quantization_config,
    device_map="auto",
    trust_remote_code=True
)

print("模型加载完成！")
print(f"模型设备: {model.device}")
print(f"显存占用: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")

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
    
    print(f"\n收到审计请求，代码长度: {len(prompt)}")
    print("开始推理...")
    
    # 生成回复
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=2048,
            temperature=0.2,
            do_sample=True,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 提取助手回复
    assistant_response = response.split("Assistant:")[-1].strip()
    
    print(f"推理完成，响应长度: {len(assistant_response)}")
    
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
    return jsonify({
        "status": "ok",
        "device": str(model.device),
        "memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB"
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("优化版服务器启动成功！")
    print("使用 8-bit 量化，完全运行在 GPU 上")
    print("API 地址: http://localhost:8000/v1/chat/completions")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=8000, debug=False)
