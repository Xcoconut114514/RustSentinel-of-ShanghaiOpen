# 使用 Ollama 运行 RustSentinel

## 步骤 1：安装 Ollama

1. 下载 Ollama for Windows：https://ollama.com/download
2. 安装后会自动启动服务

## 步骤 2：导入模型

```bash
# 将下载的模型转换为 Ollama 格式
ollama create deepseek-audit -f Modelfile
```

创建 Modelfile（在项目根目录）：
```
FROM ./model/deepseek-r1
```

## 步骤 3：运行模型

```bash
ollama run deepseek-audit
```

## 步骤 4：修改代码

将 `src/app_gradio.py` 中的 base_url 改为：
```python
client = OpenAI(api_key="EMPTY", base_url="http://localhost:11434/v1")
```

## 步骤 5：启动界面

```bash
cd src
python app_gradio.py
```
