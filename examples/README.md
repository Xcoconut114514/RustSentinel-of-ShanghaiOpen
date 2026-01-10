# 使用示例

本目录包含 RustSentinel 的各种使用示例。

## 示例列表

### 1. vulnerable_bank.rs
一个包含安全漏洞的 Solana 智能合约示例。

**漏洞类型**: Signer 检查缺失

**问题描述**: 
这个银行合约的 `withdraw` 函数没有验证账户所有者的签名，导致任何人都可以从任意账户提取资金。

**学习要点**:
- 理解 Solana 账户权限验证的重要性
- 学习如何使用 `Signer` 类型而非 `AccountInfo`
- 掌握正确的权限检查模式

### 2. basic_audit.py (即将添加)
基本的命令行审计脚本示例。

### 3. batch_audit.py (即将添加)
批量审计多个文件的示例。

### 4. api_integration.py (即将添加)
如何将 RustSentinel 集成到现有项目的示例。

## 如何使用示例

### 审计 vulnerable_bank.rs

#### 方法 1: 使用 Web 界面

1. 启动 RustSentinel:
   ```bash
   python src/app_gradio.py
   ```

2. 访问 http://localhost:8501

3. 复制 `vulnerable_bank.rs` 的内容到输入框

4. 点击"开始审计"按钮

5. 查看生成的审计报告

#### 方法 2: 使用 Python API

```python
from openai import OpenAI

# 读取示例文件
with open("examples/vulnerable_bank.rs", "r") as f:
    code = f.read()

# 连接本地模型
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

# 执行审计
response = client.chat.completions.create(
    model="deepseek-audit",
    messages=[
        {"role": "system", "content": "你是一个 Solana 安全审计专家。"},
        {"role": "user", "content": f"请审计这段代码：\n\n{code}"}
    ],
    temperature=0.1
)

# 打印结果
print(response.choices[0].message.content)
```

#### 方法 3: 使用命令行工具（即将推出）

```bash
rustsentinel audit examples/vulnerable_bank.rs --output report.md
```

## 预期输出示例

```markdown
### 风险等级
严重

### 发现的漏洞

#### 漏洞 1: 缺少 Signer 权限检查
**严重程度**: 严重

**漏洞描述**: 
在 `withdraw` 函数中，`from` 账户使用了 `AccountInfo<'info>` 类型而非 `Signer<'info>`，
这意味着任何人都可以构造交易从其他人的账户中提取资金，无需账户所有者的签名授权。

**攻击原理**: 
攻击者可以：
1. 构造一个 withdraw 交易
2. 将 `from` 参数设置为受害者的账户地址
3. 将 `to` 参数设置为攻击者的账户地址
4. 提交交易，成功盗取受害者的资金

**修复建议**: 
将 `from` 账户的类型从 `AccountInfo` 改为 `Signer`，确保只有账户所有者才能发起提款操作。

**修复代码**: 
\`\`\`rust
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut)]
    pub from: Signer<'info>,  // 改为 Signer 类型
    #[account(mut)]
    pub to: AccountInfo<'info>, 
    pub system_program: Program<'info, System>,
}
\`\`\`

### 总体评估
这个合约存在严重的权限验证漏洞，在生产环境中部署将导致资金被盗。
建议立即修复权限检查问题，并进行全面的安全审计。
```

## 贡献示例

欢迎提交更多示例！请确保：

1. 代码有清晰的注释
2. 包含漏洞说明
3. 提供预期的审计结果
4. 遵循项目代码规范

提交 PR 前请参考 [贡献指南](../README.md#贡献指南)。
