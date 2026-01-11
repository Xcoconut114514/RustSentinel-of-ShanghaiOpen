"""
使用 Ollama 的推理服务器
更快的推理速度，更好的 GPU 支持
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Ollama API 配置
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-coder:6.7b"

print("=" * 50)
print("使用 Ollama 推理引擎")
print(f"模型: {MODEL_NAME}")
print(f"API: {OLLAMA_API}")
print("=" * 50)

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
    print("开始推理（使用 Ollama）...")
    
    try:
        # 调用 Ollama API
        response = requests.post(
            OLLAMA_API,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 2048
                }
            },
            timeout=300  # 5 分钟超时
        )
        
        if response.status_code == 200:
            result = response.json()
            assistant_response = result.get('response', '')
            
            print(f"推理完成，响应长度: {len(assistant_response)}")
            
            return jsonify({
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": assistant_response
                    }
                }]
            })
        else:
            error_msg = f"Ollama API 错误: {response.status_code}"
            print(error_msg)
            return jsonify({"error": error_msg}), 500
            
    except requests.exceptions.Timeout:
        error_msg = "推理超时（5分钟）"
        print(error_msg)
        return jsonify({"error": error_msg}), 504
    except Exception as e:
        error_msg = f"错误: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500

@app.route('/health', methods=['GET'])
def health():
    try:
        # 检查 Ollama 是否运行
        response = requests.get("http://localhost:11434", timeout=2)
        ollama_status = "running" if response.status_code == 200 else "error"
    except:
        ollama_status = "not running"
    
    return jsonify({
        "status": "ok",
        "engine": "Ollama",
        "model": MODEL_NAME,
        "ollama_status": ollama_status
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Ollama 服务器启动成功！")
    print("使用 Ollama 推理引擎，速度更快")
    print("API 地址: http://localhost:8000/v1/chat/completions")
    print("="*50 + "\n")
    
    # 检查 Ollama 是否运行
    try:
        response = requests.get("http://localhost:11434", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama 服务正常运行")
        else:
            print("⚠️  警告: Ollama 服务可能未运行")
    except:
        print("❌ 错误: 无法连接到 Ollama")
        print("   请确保 Ollama 正在运行")
        print("   如果未运行，Ollama 会自动启动")
    
    print()
    app.run(host='0.0.0.0', port=8000, debug=False)
