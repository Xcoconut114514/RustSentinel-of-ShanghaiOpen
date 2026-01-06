# 测试说明

本目录包含 RustSentinel 的测试用例。

## 测试结构

```
tests/
├── README.md              # 本文件
├── test_basic.py         # 基础功能测试（待添加）
├── test_api.py           # API 测试（待添加）
└── test_models.py        # 模型集成测试（待添加）
```

## 运行测试

### 前置条件

1. 确保已安装所有依赖：
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov  # 测试依赖
   ```

2. 确保 vLLM 服务正在运行：
   ```bash
   vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
       --port 8000 \
       --model-name deepseek-audit
   ```

### 运行所有测试

```bash
# 在项目根目录下
pytest tests/ -v
```

### 运行特定测试

```bash
# 运行基础测试
pytest tests/test_basic.py -v

# 运行 API 测试
pytest tests/test_api.py -v
```

### 生成测试覆盖率报告

```bash
pytest tests/ --cov=src --cov-report=html
# 在浏览器中打开 htmlcov/index.html 查看覆盖率
```

## 测试计划

### 单元测试（待实现）

- [ ] Prompt 模板功能测试
- [ ] 配置加载测试
- [ ] 错误处理测试

### 集成测试（待实现）

- [ ] vLLM API 连接测试
- [ ] 端到端审计流程测试
- [ ] 流式输出测试

### 性能测试（待实现）

- [ ] 单次审计延迟测试
- [ ] 并发处理能力测试
- [ ] 显存占用测试

## 贡献测试用例

如果您想为项目添加测试，请：

1. 在 `tests/` 目录下创建测试文件
2. 使用 `pytest` 框架编写测试
3. 确保测试可重复运行
4. 添加必要的文档注释
5. 提交 Pull Request

### 测试规范

```python
import pytest
from openai import OpenAI

def test_audit_basic():
    """测试基本审计功能"""
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")
    
    code = """
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        Ok(())
    }
    """
    
    response = client.chat.completions.create(
        model="deepseek-audit",
        messages=[
            {"role": "system", "content": "你是安全审计专家"},
            {"role": "user", "content": code}
        ]
    )
    
    assert response.choices[0].message.content is not None
    assert len(response.choices[0].message.content) > 0
```

## 持续集成

本项目使用 GitHub Actions 进行 CI/CD（计划中）。

每次提交都会自动运行测试套件，确保代码质量。

---

测试是确保软件质量的重要环节，欢迎贡献！
