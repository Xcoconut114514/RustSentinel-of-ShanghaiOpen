import gradio as gr
from openai import OpenAI

# 1. 连接本地 C500 大模型
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

def smart_audit(code_snippet):
    if not code_snippet:
        return "⚠️ 请先粘贴代码！"
    try:
        system_prompt = "你是一个智能合约安全专家，请分析代码漏洞（逻辑漏洞/权限绕过），输出Markdown格式的：风险等级、攻击原理、修复代码。"
        response = client.chat.completions.create(
            model="deepseek-audit",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": code_snippet}],
            temperature=0.2, max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 错误: {str(e)}"

# 2. 界面配置
with gr.Blocks(title="RustSentinel", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ RustSentinel 智能审计终端 (C500 驱动)")
    with gr.Row():
        inp = gr.Textbox(label="输入 Rust 代码", lines=15, placeholder="粘贴代码...")
        btn = gr.Button("🚀 开始审计", variant="primary")
    out = gr.Markdown(label="审计报告")
    btn.click(fn=smart_audit, inputs=inp, outputs=out)

# 3. 【关键】手工指定你的专属路径
# 根据你的截图，你的 ID 是 vm-Tla98pdzbMRK1Js5
MY_ROOT_PATH = "/vm-Tla98pdzbMRK1Js5/proxy/8501/"

print(f"DEBUG: Root Path 强制设置为: {MY_ROOT_PATH}")

demo.launch(
    server_name="0.0.0.0", 
    server_port=8501, 
    share=False,
    root_path=MY_ROOT_PATH  # 告诉 Gradio 它的真实地址
)
