"""
带数据库支持的推理服务器
保存审计历史记录到 MySQL
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# 数据库配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'rustsentinel',
    'port': 3306
}

def get_db_connection():
    """获取数据库连接"""
    return mysql.connector.connect(**DB_CONFIG)

def init_database():
    """初始化数据库表"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建审计历史表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code TEXT NOT NULL,
            result TEXT NOT NULL,
            code_length INT,
            result_length INT,
            inference_time FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 数据库表初始化完成")

# 启动时初始化数据库
try:
    init_database()
except Exception as e:
    print(f"⚠️  数据库初始化失败: {e}")
    print("   请确保 MySQL 服务正在运行，数据库 'rustsentinel' 已创建")

# 导入模型相关
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import time

print("正在加载模型（8-bit 量化版本）...")
model_path = "./model/deepseek-r1"

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False,
)

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quantization_config,
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
    
    # 提取用户代码（去掉 system prompt）
    user_code = ""
    for msg in messages:
        if msg['role'] == 'user':
            user_code = msg['content']
            break
    
    print(f"\n收到审计请求，代码长度: {len(user_code)}")
    print("开始推理...")
    
    start_time = time.time()
    
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
    assistant_response = response.split("Assistant:")[-1].strip()
    
    inference_time = time.time() - start_time
    
    print(f"推理完成，耗时: {inference_time:.2f} 秒")
    
    # 保存到数据库
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_history 
            (code, result, code_length, result_length, inference_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            user_code,
            assistant_response,
            len(user_code),
            len(assistant_response),
            inference_time
        ))
        
        conn.commit()
        audit_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        print(f"✅ 审计记录已保存，ID: {audit_id}")
        
    except Exception as e:
        print(f"⚠️  保存到数据库失败: {e}")
    
    return jsonify({
        "choices": [{
            "message": {
                "role": "assistant",
                "content": assistant_response
            }
        }]
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """获取审计历史记录"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        offset = (page - 1) * page_size
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 获取总数
        cursor.execute("SELECT COUNT(*) as total FROM audit_history")
        total = cursor.fetchone()['total']
        
        # 获取分页数据
        cursor.execute("""
            SELECT id, code, result, code_length, result_length, 
                   inference_time, created_at
            FROM audit_history
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (page_size, offset))
        
        records = cursor.fetchall()
        
        # 转换日期格式
        for record in records:
            record['created_at'] = record['created_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "total": total,
            "page": page,
            "page_size": page_size,
            "records": records
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<int:id>', methods=['GET'])
def get_history_detail(id):
    """获取单条审计记录详情"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, code, result, code_length, result_length,
                   inference_time, created_at
            FROM audit_history
            WHERE id = %s
        """, (id,))
        
        record = cursor.fetchone()
        
        if record:
            record['created_at'] = record['created_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        if record:
            return jsonify(record)
        else:
            return jsonify({"error": "记录不存在"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<int:id>', methods=['DELETE'])
def delete_history(id):
    """删除审计记录"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM audit_history WHERE id = %s", (id,))
        
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected > 0:
            return jsonify({"message": "删除成功"})
        else:
            return jsonify({"error": "记录不存在"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    # 检查数据库连接
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM audit_history")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        db_status = f"ok ({count} records)"
    except:
        db_status = "error"
    
    return jsonify({
        "status": "ok",
        "device": str(model.device),
        "memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
        "database": db_status
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("带数据库支持的服务器启动成功！")
    print("使用 8-bit 量化，完全运行在 GPU 上")
    print("审计记录将自动保存到 MySQL 数据库")
    print("API 地址: http://localhost:8000/v1/chat/completions")
    print("历史记录: http://localhost:8000/api/history")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=8000, debug=False)
