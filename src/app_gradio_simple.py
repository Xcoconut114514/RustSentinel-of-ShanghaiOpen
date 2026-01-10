import gradio as gr
from openai import OpenAI

# 连接本地模型
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

def smart_audit(code_snippet):
    print(f"\n收到审计请求，代码长度: {len(code_snippet) if code_snippet else 0}")
    
    if not code_snippet or code_snippet.strip() == "":
        return "⚠️ 请先粘贴代码！"
    
    try:
        print("正在调用 API...")
        system_prompt = "你是一个智能合约安全专家，请分析代码漏洞（逻辑漏洞/权限绕过），输出Markdown格式的：风险等级、攻击原理、修复代码。"
        
        response = client.chat.completions.create(
            model="deepseek-audit",
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": code_snippet}
            ],
            temperature=0.2, 
            max_tokens=2048
        )
        
        result = response.choices[0].message.content
        print(f"API 返回成功，长度: {len(result)}")
        return result
        
    except Exception as e:
        error_msg = f"❌ 错误: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg

# 创建界面
with gr.Blocks(title="RustSentinel") as demo:
    gr.Markdown("# 🛡️ RustSentinel 智能审计终端")
    
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(
                label="输入 Rust 代码", 
                lines=15, 
                placeholder="粘贴代码...",
                interactive=True
            )
            btn = gr.Button("🚀 开始审计", variant="primary", size="lg")
        
        with gr.Column():
            out = gr.Markdown(label="审计报告", value="等待审计...")
    
    # 绑定点击事件
    btn.click(fn=smart_audit, inputs=inp, outputs=out)
    
    print("\n界面组件已创建，按钮事件已绑定")

print("正在启动服务器...")
demo.launch(
    server_name="0.0.0.0", 
    server_port=8502,  # 换个端口避免冲突
    share=False
)
