# 贡献指南

感谢您对 RustSentinel 项目的关注！我们欢迎所有形式的贡献。

## 🎯 贡献方式

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ✨ 开发新功能
- 🧪 编写测试用例

## 📋 开始之前

### 1. 查看现有 Issue

在开始工作前，请先查看 [Issues](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues)：

- 避免重复工作
- 了解项目当前需求
- 寻找适合自己的任务

### 2. Fork 仓库

1. 点击右上角的 "Fork" 按钮
2. 克隆您的 Fork 到本地：
   ```bash
   git clone https://github.com/YOUR_USERNAME/RustSentinel-of-ShanghaiOpen.git
   cd RustSentinel-of-ShanghaiOpen
   ```

### 3. 设置开发环境

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest black flake8 mypy
```

## 🔄 工作流程

### 1. 创建分支

从 `main` 分支创建一个新的特性分支：

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b bugfix/issue-number-description
```

分支命名规范：
- `feature/xxx` - 新功能
- `bugfix/xxx` - Bug 修复
- `docs/xxx` - 文档更新
- `refactor/xxx` - 代码重构
- `test/xxx` - 测试相关

### 2. 进行开发

#### 代码规范

- **Python**: 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- **格式化**: 使用 `black` 格式化代码
- **类型注解**: 尽可能添加类型提示
- **注释**: 使用中文注释，清晰简洁

**格式化代码**:

```bash
# 格式化所有 Python 文件
black src/ tests/

# 检查代码风格
flake8 src/ tests/

# 类型检查
mypy src/
```

#### 提交信息规范

使用清晰的中文提交信息：

```bash
git commit -m "feat: 添加批量审计功能"
git commit -m "fix: 修复显存溢出问题 (#123)"
git commit -m "docs: 更新部署文档"
git commit -m "refactor: 重构 Prompt 模板系统"
```

提交类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 3. 编写测试

为新功能添加测试用例：

```python
# tests/test_new_feature.py
import pytest
from src.your_module import your_function

def test_your_function():
    """测试您的新功能"""
    result = your_function("input")
    assert result == "expected_output"
```

运行测试：

```bash
pytest tests/ -v
```

### 4. 更新文档

如果您的更改影响了用户使用方式，请更新相关文档：

- `README.md` - 主文档
- `docs/api.md` - API 文档
- `docs/deployment.md` - 部署文档
- `examples/` - 使用示例

### 5. 推送更改

```bash
# 推送到您的 Fork
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request

1. 访问您的 Fork 页面
2. 点击 "Pull Request" 按钮
3. 填写 PR 描述：

```markdown
## 更改说明
简要描述您的更改内容

## 相关 Issue
关闭 #123

## 更改类型
- [ ] Bug 修复
- [x] 新功能
- [ ] 文档更新
- [ ] 代码重构

## 测试
- [x] 添加了新的测试用例
- [x] 所有测试通过
- [x] 已手动验证

## 截图（如适用）
添加截图展示您的更改

## 检查清单
- [x] 代码遵循项目规范
- [x] 已添加必要的注释
- [x] 已更新相关文档
- [x] 测试已通过
```

## 🐛 报告 Bug

### 创建 Bug 报告

使用 [Bug 报告模板](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues/new?template=bug_report.md)

**请包含**:

1. **环境信息**:
   - 操作系统
   - Python 版本
   - GPU 型号
   - 相关依赖版本

2. **复现步骤**:
   - 详细的操作步骤
   - 最小化的复现代码

3. **预期行为**:
   - 您期望发生什么

4. **实际行为**:
   - 实际发生了什么
   - 错误信息/日志

5. **额外信息**:
   - 截图
   - 相关配置文件

## 💡 功能建议

使用 [功能请求模板](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues/new?template=feature_request.md)

**请说明**:

1. **问题描述**: 您遇到了什么问题？
2. **解决方案**: 您建议的解决方案是什么？
3. **替代方案**: 是否考虑过其他方案？
4. **使用场景**: 这个功能的使用场景是什么？

## 📝 文档贡献

文档同样重要！您可以：

- 修正拼写/语法错误
- 添加使用示例
- 改进说明清晰度
- 翻译文档（计划支持英文）

## 🎨 代码审查

所有 PR 都需要经过审查：

- **响应时间**: 我们会在 2-3 个工作日内响应
- **讨论**: 开放友好的讨论代码改进
- **修改**: 根据反馈进行必要的修改
- **合并**: 审查通过后会合并您的 PR

## ❓ 问题与帮助

遇到问题？

- 📖 查看 [文档](../README.md)
- 🔍 搜索 [现有 Issues](https://github.com/Xcoconut114514/RustSentinel-of-ShanghaiOpen/issues)
- 💬 创建新的 Issue
- 📧 邮件联系: 2819404727@qq.com

## 🏆 贡献者

感谢所有贡献者！您的贡献将被记录在项目中。

## 📜 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们承诺：

- ✅ 尊重不同的观点和经验
- ✅ 接受建设性的批评
- ✅ 关注对社区最有利的事情
- ✅ 对其他社区成员表示同理心

### 不可接受的行为

- ❌ 使用性化的语言或图像
- ❌ 人身攻击或侮辱性评论
- ❌ 骚扰（公开或私下）
- ❌ 未经许可发布他人的私人信息
- ❌ 其他不道德或不专业的行为

## 📄 许可证

通过贡献，您同意您的贡献将采用与项目相同的 [MIT License](../LICENSE)。

---

再次感谢您的贡献！🎉
