## DSN: A Workflow-Driven Conversational Computer Control System Framework

**English** | [简体中文](https://github.com/ccjjfdyqlhy/DSN-pre/blob/main/README_zh-CN.md)

**DSN** is an innovative interactive prompting framework that combines the power of large language models and computer utilities to create an intelligent and engaging conversational control experience.
**This repository is an early preview branch, synchronized with the internal development branch on 2024/11/15.**  
**Main version Rev2_1.1.2, API version Rev2_IOmod_2.2.0**  

**Updates:**

This update allows a single DSN instance to control multiple Windows devices simultaneously, significantly reducing the performance burden on controlled devices and expanding the control domain.

* Moved numerous action functions to the client [DodoUI](https://github.com/ccjjfdyqlhy/DodoUI), including instruction execution and search logic, achieving **complete separation of server and client**.
* Added **control functions for WeChat**.  Can access contacts, send messages on behalf of the user, automatically reply to specific messages, and provide modification suggestions for user messages based on context.
* Made **all initialization prompts public**.
* Added a **TTS control switch on the client**, allowing users to turn off TTS to improve inference speed.
* Added **long-term memory** (for models with sufficiently long context windows), allowing a configurable amount of streamlined memory to be loaded after restart.
* Introduced **memo optimization**, designed to simply enhance small-scale models' understanding weight of certain prompts. Can be manually adjusted.
* Completely **rewrote the action feedback section**, separating it from the text message channel to prevent the main model from incorrectly separating action results from requests (low probability event).


**Coming in the next version:**

* **Pure vision-driven RPA**, further expanding the system's control range by directly controlling keyboard and mouse operations on the GUI.
* **Multi-user support**, using biometric identification to establish independent profiles for different users and provide more tailored responses. Information learned from each user will be stored independently in profile files.
* **Improved execution logic**, using PowerShell scripts for true asynchronous operation and automatically finding suitable applications on the computer to open corresponding files.
* **Automatic installation and configuration of some software**, eliminating the tedious steps of manual environment configuration.
* **Multimodal input on the client side**.

**Feature Overview:**

* **Understands and responds to your natural language requests** - You can ask any question, and it will try its best to fulfill your request.
* **Comprehensive control of multiple computers** - The framework can automatically execute code or commands on your different computers, handling your requests directly and efficiently.
* **Search for files and information** - Easily find files across your entire disk or search for information on the web.
* **Autonomous learning** - DSN continuously learns from your interactions, improving its responses over time.
* **Integration with external applications** - Use the API to extend DSN's functionality.
* **Supports local model deployment** - Run DSN offline using your custom models.

**Features:**

* **Voice Interaction:** DSN supports pure voice interaction, although this feature currently only runs on the server-side and is not yet implemented for client-side voice input.
* **Custom Prompts:**  Edit your own prompts in the `custom_prompt.py` file to personalize the AI.
* **Self-Correction:** DSN can gracefully handle errors and automatically perform environment configuration and self-correction.
* **Experience Acceleration:** Recording key points of conversations in the memo file `memo.txt` can make action execution more efficient and faster.
* **Visual Understanding:** Allows DSN to "see" and analyze images from your camera or local files. Only runs on the server-side; not currently supported on the client.
* **Text-to-Speech:** Choose between two TTS solutions:
    * **ChatTTS API:** Access high-quality voices through the local ChatTTS API.
    * **DSN-Vocal:** Leverage the integrated DSN-Vocal, a GPT-SoVITS-based multi-emotional neural network text-to-speech framework for faster, local text-to-speech processing.
* **API Support:** Embed DSN into any application using its API. Some API client examples with varying levels of implementation difficulty are provided in `/examples/`. Dodo UI's code is also available for reference.
* **Memory:** Even after restarting the control system framework acting as the server, DSN retains memory of previous conversations, providing a more personalized experience.


## Getting Started

***Note: This setup guide may not be exhaustive.  Please submit an issue for specific problems.***

You can download a packaged Python runtime from [here](https://github.com/ccjjfdyqlhy/DSN-pre/releases), or you can install the dependency libraries yourself.

**1. Prerequisites:**

* **Python 3.11+:** Install Python (3.11.2 recommended) from the [official website](https://www.python.org/).
* **Google Cloud Platform API Key (for online model access):** You can get a free trial API key [here](https://aistudio.google.com/app/apikey).
* **Everything Search Engine (for file searching):** Download the full version from their [website](https://www.voidtools.com/downloads) and install it in the `binaries` folder of this cloned repository.
* **Paraformer-zh (for speech recognition):** Download from [Modelscope](https://www.modelscope.cn/models/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch/files) or [HuggingFace](https://huggingface.co/funasr/paraformer-zh) into the `instances\\paraformer` folder.
* **Moondream (for local image recognition):** Download from [HuggingFace](https://huggingface.co/vikhyatk/moondream2) into the `instances\\moondream` folder.
* **Pre-built ChatTTS (alternative TTS solution):**  Being adapted, will be supported in the future.


**2. Installation:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ccjjfdyqlhy/DSN-pre.git
   cd DSN-pre
   ```
2. **Install the necessary packages in `install_before_requirements.txt`.**

3. **Download local model (optional):**
   * Navigate to the `instances\\gemma-2` folder within the cloned repository.
   * Download the gemma-2-modified.nt model and place it in the folder.
4. **Install dependencies:**
   * Install the pip dependency files in the installing folder in sequence:
   ```bash
   cd installing
   pip install -r requirements-python3.9.13.txt
   pip install -r requirements-python3.11.2.txt
   ```
5. **Download and configure TTS model resources:**
   * Download the TTS model package from [here](https://github.com/ccjjfdyqlhy/DSN-pre/releases) into the `TTS_models` folder. You can use the directory structure of this folder as a template and use your own trained GPT-SoVITS model for TTS inference.
   * Set the model folder path and the model used in `config-ui.py`.

**3. Configuration:**

* **Use the configuration tool to generate `config.py`:**
   ```bash
   python config-ui.py
   ```
   * This will open a webUI where you can adjust various settings for DSN.
   * Once finished, the tool will generate a `config.py` file based on your choices.
* **Further customize settings in `config.py` if necessary:**
    * You can manually edit the `config.py` file to fine-tune settings related to voice control, text-to-speech, visual understanding, local/online models, and more.

**4. Start DSN:**

* **Run locally only (no UI, supports multimodal input):**
   ```bash
   ./runtimes/python311/python.exe main.py
   ```
* **Start as a server (supports multiple clients simultaneously):**
   ```bash
   ./runtimes/python311/python.exe api.py backend
   ```

**Notes:**

* **Caution: You must read and agree to all terms of use in the `LICENCE` file before starting to use.**
* This project is under active development, and some features are not yet fully implemented or are buggy. Community contributions are welcome.
