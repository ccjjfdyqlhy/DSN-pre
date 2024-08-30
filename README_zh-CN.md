## DSN: 基于深度流式神经网络的控制系统框架

[English](https://github.com/ccjjfdyqlhy/DSN-pre/blob/main/README.md) | **简体中文**  

**DSN** 是一个强大且创新的交互式提示框架，它结合了大模型和计算机实用程序的能力，创造出真正智能且引人入胜的对话控制体验。  
**当前仓库是本项目的早期预览分支，在2024/8/30与核心分支同步。**

**DSN 可以：**

* **理解并响应你的自然语言请求** - 你可以询问任何问题，它会尽力满足你的要求。
* **全面控制计算机** - 该框架可以自动在你的电脑上执行代码或命令，直接处理你的请求。
* **搜索文件和信息** - 轻松地在全盘查找文件或在网络上查找信息。
* **从你的交互中学习** - DSN 会不断地从你的交互中学习，随着时间的推移改进其响应。
* **与外部应用程序集成** - 使用 API 以扩展 DSN 的功能。
* **支持本地模型部署** - 使用你的自定义模型离线运行 DSN。

**特性：**  
* **语音控制：** 与 DSN 对话，让它听到你的指令！
* **本地模型支持：** 使用你自己的自定义模型来保护隐私和离线访问。
* **高级搜索功能：** 按名称、类型或关键字搜索文件。
* **可自定义设置：** 通过调整 `config.py` 文件中的设置来定制 DSN 以满足你的需求，可以使用 `config-ui.py` 工具轻松生成和修改该文件。
* **可自定义提示词：** 可以在 `custom_prompt.py` 文件中编辑你自己的提示词，以达到个性化AI的效果。
* **错误处理：** DSN 可以优雅地处理错误并自动执行配置环境、自我纠正等操作。
* **经验加速：** 在备忘录文件 `memo.txt` 中记录对话的要点，可以使动作执行更高效、更快速。
* **视觉理解：** 允许 DSN 从你的相机或本地文件中“看到”和分析图像。
* **文本转语音：** 在两种 TTS 解决方案之间进行选择：
    * **ChatTTS API：** 通过本地 ChatTTS API 访问高质量的声音。
    * **DSN-Vocal (GPT-SoVITS)：** 利用集成的 DSN-Vocal，这是一个基于 GPT-SoVITS 的多情感神经网络文本转语音框架，用于更快、本地的文本转语音处理。
* **API 支持：** 使用其 API 将 DSN 嵌入到任何应用程序中。`/examples/api_client.py` 中提供了一个 API 客户端示例。

## 马上开始：

你可以从[这里](https://github.com/ccjjfdyqlhy/DSN-pre/releases)下载打包好的Python运行时，或者你也可以自行安装依赖库。

**1. 先决条件：**  
* **Python 3.11+：** 从 [官方网站](https://www.python.org/)安装 Python（建议使用 3.11.2）。
* **Google Cloud Platform API 密钥（用于在线模型访问）：** 你可以在[此处](https://aistudio.google.com/app/apikey)获取免费试用 API 密钥。
* **Everything 搜索引擎（用于文件搜索）：** 从他们的 [网站](https://www.voidtools.com/downloads) 下载完整版本，然后将其安装在此克隆存储库的 `binaries` 文件夹中。
* **Paraformer-zh（用于语音识别）：** 从 [Modelscope](https://www.modelscope.cn/models/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch/files) 或 [HuggingFace](https://huggingface.co/funasr/paraformer-zh) 下载到 `instances\\paraformer` 文件夹中。  
* **Moondream（用于本地图像识别）：** [HuggingFace](https://huggingface.co/vikhyatk/moondream2) 下载到 `instances\\moondream` 文件夹中。
* **已经构建好的ChatTTS（另外一种TTS解决方案）：** 正在适配中，将来支持

**2. 安装：**

1. **克隆存储库：** 
   ```bash
   git clone https://github.com/ccjjfdyqlhy/DSN-pre.git
   ```
2. **在 `install_before_requirements.txt` 中安装必要的软件包。**

3. **下载 DSN-local.NT 模型（可选）：**
   * 导航到克隆存储库中的 `instances\\DSN` 文件夹。
   * 下载 DSN-local.NT 模型并将其放置在文件夹中。
4. **安装依赖项：**
   ```bash
   pip install -r requirements.txt
   ```
5、**下载并配置TTS模型资源：**
   * 从[这里](https://github.com/ccjjfdyqlhy/DSN-pre/releases)下载TTS模型包到 `TTS_models` 文件夹。你可以把该文件夹当作样板，使用自己训练的GPT-SoVITS模型进行TTS推理。
   * 在 `config-ui.py` 中设定使用的模型文件夹路径和使用的模型。

**3. 配置：**

* **使用配置工具生成 `config.py`：**
   ```bash
   python config-ui.py 
   ```
   * 这将打开一个用户界面，你可以在其中调整 DSN 的各种设置。
   * 完成后，该工具将根据你的选择生成 `config.py` 文件。
* **如有必要，在 `config.py` 中进一步自定义设置：**
    * 你可以手动编辑 `config.py` 文件，以微调与语音控制、文本转语音、视觉理解、本地/在线模型等相关的设置。

**4. 启动 DSN：**
* **运行程序：**
   ```bash
   cd DSN-pre
   python DSN.Launch.py
   ```

**补充说明：**

* **注意：在开始使用之前，你必须阅读并同意 `LICENCE` 文件中的所有使用条款。**
* 本项目正在积极开发中，部分功能尚未完全实现或漏洞百出，欢迎社区捉虫。
