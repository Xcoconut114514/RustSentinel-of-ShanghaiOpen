# 使用 Text Generation WebUI 运行

## 优点
- 图形化界面，易于使用
- Windows 支持完善
- 自带 API 服务器

## 安装步骤

1. 下载 Text Generation WebUI：
   ```bash
   git clone https://github.com/oobabooga/text-generation-webui
   cd text-generation-webui
   ```

2. 运行一键安装脚本：
   ```bash
   start_windows.bat
   ```

3. 在 WebUI 中加载模型：
   - 打开 http://localhost:7860
   - 在 Model 标签页选择你的模型路径
   - 点击 Load

4. 启用 API：
   - 在启动参数中添加 `--api`
   - 重启服务

5. 修改 RustSentinel 代码：
   ```python
   client = OpenAI(api_key="EMPTY", base_url="http://localhost:5000/v1")
   ```
