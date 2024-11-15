## DSN: 工作流驱动的对话式计算机控制系统框架

[English](https://github.com/ccjjfdyqlhy/DSN-pre/blob/main/README.md) | **简体中文**  

**DSN** 是一个创新的交互式提示框架，它结合了大模型和计算机实用程序的能力，创造出智能且引人入胜的对话控制体验。  
**当前仓库是本项目的早期预览分支，在2024/11/15与内部开发分支同步。**
**main 版本 Rev2_1.1.2，API 版本 Rev2_IOmod_2.2.0**  

**更新内容：**  

总的来说，本次更新允许单个 DSN 实例同时支配多台运行 Windows 的设备，并大量减轻受控制设备的性能负担、拓展控制领域。  
* 将大量的动作函数移动到客户端 [DodoUI](https://github.com/ccjjfdyqlhy/DodoUI) ，其中包括指令执行、搜索相关逻辑等，实现**服务端与客户端彻底分离**。  
* 增加了**对微信 (WeChat) 的控制函数**。能够访问通讯录、代为用户发送消息或针对特定的消息自动回复，以及根据上下文对用户的消息提供修改建议。  
* 公开了**全部初始化提示词**。
* 在客户端添加了**TTS控制开关**，从而使用户能够通过关掉 TTS 以提高推理速率。  
* 增加了**长期记忆** (适用于具有足够长上下文窗口的模型)，使一部分可配置大小的精简记忆能够在重启之后被加载。
* 提出了**备忘录优化**，旨在简易增强小规模模型对部分提示词的理解权重。可以人为调整。
* 彻底**重写了动作反馈部分**，将其与文本消息通道分离，以避免主模型错误地分离动作结果与需求 (小概率事件) 。

**将在下个版本中支持：**
* **纯视觉驱动的RPA**，通过直接控制键盘和鼠标操作 GUI ，进一步拓展系统能控制的范围。
* **多用户**，通过生物识别为不同的用户建立相互独立的档案，并针对不同用户的需求提供更加适合的响应。从每个用户处学习到的信息将独立存储在档案文件中。
* **更好的执行逻辑**，通过 PowerShell 脚本实现真异步运行，并自动在电脑上查找适合的应用程序打开对应的文件。
* **部分软件的自动安装与配置**，省去手动配置环境的繁杂步骤。
* **客户端使用多模态输入**。

**功能概述：**
* **理解并响应你的自然语言请求** - 你可以询问任何问题，它会尽力满足你的要求。
* **全面控制多台计算机** - 该框架可以自动在你的不同电脑上执行代码或命令，直接而高效地处理你的请求。
* **搜索文件和信息** - 轻松地在全盘查找文件或在网络上查找信息。
* **自主学习** - DSN 会不断地从与你的交互中学习，随着时间的推移改进其响应。
* **与外部应用程序集成** - 使用 API 以扩展 DSN 的功能。
* **支持本地模型部署** - 使用你的自定义模型离线运行 DSN。

**特性：**
* **语音交互：** DSN 支持纯语音交互，不过这个功能目前仅能在服务端运行，在客户端上暂时无法实现语音输入。
* **自定义提示词：** 可以在 `custom_prompt.py` 文件中编辑你自己的提示词，以达到个性化 AI 的效果。
* **自纠错：** DSN 可以优雅地处理错误并自动执行配置环境、自我纠正等操作。
* **经验加速：** 在备忘录文件 `memo.txt` 中记录对话的要点，可以使动作执行更高效、更快速。
* **视觉理解：** 允许 DSN 从你的相机或本地文件中“看到”和分析图像。仅能在服务端运行，客户端暂未支持。
* **文本转语音：** 在两种 TTS 解决方案之间进行选择：
    * **ChatTTS API：** 通过本地 ChatTTS API 访问高质量的声音。
    * **DSN-Vocal：** 利用集成的 DSN-Vocal，这是一个基于 GPT-SoVITS 的多情感神经网络文本转语音框架，用于更快、本地的文本转语音处理。
* **API 支持：** 使用其 API 将 DSN 嵌入到任何应用程序中。`/examples/` 中提供了一些实现难度不一的 API 客户端示例。Dodo UI 的代码也可供参考。
* **记忆：** 即使重新启动作为服务端的控制系统框架，DSN 也依旧具有之前对话的记忆，提供更加个性化的体验。

## 马上开始

***注意：该设置教学可能步骤不完全。欢迎针对特定问题提交 issue 。***  
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
   cd DSN-pre
   ```
2. **在 `install_before_requirements.txt` 中安装必要的软件包。**

3. **下载本地模型（可选）：**
   * 导航到克隆存储库中的 `instances\\gemma-2` 文件夹。
   * 下载 gemma-2-modified.nt 模型并将其放置在文件夹中。
4. **安装依赖项：**
   * 依次安装installing文件夹中的 pip 依赖文件：
   ```bash
   cd installing
   pip install -r requirements-python3.9.13.txt
   pip install -r requirements-python3.11.2.txt
   ```
5、**下载并配置TTS模型资源：**
   * 从[这里](https://github.com/ccjjfdyqlhy/DSN-pre/releases)下载TTS模型包到 `TTS_models` 文件夹。你可以把该文件夹的目录结构当作样板，使用自己训练的GPT-SoVITS模型进行TTS推理。
   * 在 `config-ui.py` 中设定使用的模型文件夹路径和使用的模型。

**3. 配置：**

* **使用配置工具生成 `config.py`：**
   ```bash
   python config-ui.py 
   ```
   * 这将打开一个 webUI ，你可以在其中调整 DSN 的各种设置。
   * 完成后，该工具将根据你的选择生成 `config.py` 文件。
* **如有必要，在 `config.py` 中进一步自定义设置：**
    * 你可以手动编辑 `config.py` 文件，以微调与语音控制、文本转语音、视觉理解、本地/在线模型等相关的设置。

**4. 启动 DSN：**
* **仅在本地运行 (无 UI，支持多模态)：**
   ```bash
   ./runtimes/python311/python.exe main.py
   ```
* **作为服务端启动（支持多客户端同时使用）：**
	```bash
   ./runtimes/python311/python.exe api.py backend
   ```

**说明：**

* **注意：在开始使用之前，你必须阅读并同意 `LICENCE` 文件中的所有使用条款。**
* 本项目正在积极开发中，部分功能尚未完全实现或漏洞百出，欢迎社区捉虫。
