import streamlit as st
from openai import OpenAI
import time

# 1. 基础配置
st.set_page_config(page_title="RustSentinel", layout="wide", page_icon="🛡️")

# 连接本地模型
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

# 2. 侧边栏
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("🛡️ RustSentinel")
    st.success("🟢 C500 算力引擎在线")
    st.info("当前模型: DeepSeek-R1-Distill (BF16)")

# 3. 主界面
st.title("🚀 Rust 智能合约审计终端")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 输入代码")
    # 默认代码
    default_code = """use anchor_lang::prelude::*;
#[program]
pub mod insecure_bank {
    use super::*;
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        // 🚨 漏洞：没检查账户所有权，谁都能取钱！
        let from = &mut ctx.accounts.from;
        let to = &mut ctx.accounts.to;
        **from.to_account_info().try_borrow_mut_lamports()? -= amount;
        **to.to_account_info().try_borrow_mut_lamports()? += amount;
        Ok(())
    }
}"""
    code_input = st.text_area("Rust 代码:", value=default_code, height=400)

with col2:
    st.subheader("📊 审计报告")
    if st.button("开始审计 (Start Audit)", type="primary"):
        status = st.status("正在思考中...", expanded=True)
        try:
            status.write("🧠 连接 C500 大脑...")
            response = client.chat.completions.create(
                model="deepseek-audit",
                messages=[
                    {"role": "system", "content": "你是一个 Solana 安全专家。请找出代码漏洞并给出修复建议。"},
                    {"role": "user", "content": code_input}
                ],
                stream=True
            )
            
            result_area = st.empty()
            full_text = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
                    result_area.markdown(full_text + "▌")
            
            result_area.markdown(full_text)
            status.update(label="审计完成！", state="complete", expanded=False)
        except Exception as e:
            st.error(f"连接失败: {e}")
