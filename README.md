## DSN: Deep Streaming Neural Networks-based Control System Framework

**English** | [简体中文](https://github.com/ccjjfdyqlhy/DSN-pre/blob/main/README_zh-CN.md)  

**DSN** is a powerful and innovative interactive prompt framework that combines the capabilities of large language models and computer utilities, creating a truly intelligent and engaging conversational control experience.  
**The current repository is an early preview branch of this project and it's synchronized with the core branch on 2024/8/30.** 

**With DSN, you can:**

* **Understand and respond to your natural language requests** - You can ask it anything, and it will do its best to fulfill your requests.
* **Take full control of your computer** - The framework can automatically execute code or commands on your computer, directly handling your requests.
* **Search for files and information** - Effortlessly find files across your entire disk or search for information on the web.
* **Learn from your interactions** - DSN continuously learns from your interactions, improving its responses over time.
* **Integrate with external applications** - Use APIs to expand DSN's functionality.
* **Support local model deployment** - Use your custom models to run DSN offline.

**Features:**

* **Voice control:** Talk to DSN and let it hear your instructions!
* **Local model support:** Utilize your own custom models for enhanced privacy and offline access.
* **Advanced search capabilities:** Search for files by name, type, or keywords.
* **Customizable settings:** Tailor DSN to your needs by adjusting the settings in the `config.py` file, which can be easily generated and modified using the `config-ui.py` tool.
* **Customizable prompts:** Edit your own prompts in the `custom_prompt.py` file to achieve personalized AI effects.
* **Error handling:** DSN can gracefully handle errors and automatically configure the environment, self-correct, and more.
* **Experience acceleration:** Recording the main points of the conversation in the memo file `memo.txt` can make action execution more efficient and faster.
* **Visual understanding:** Allow DSN to "see" and analyze images from your camera or local files.
* **Text-to-speech:** Choose between two TTS solutions:
    * **ChatTTS API:** Access high-quality voices through the local ChatTTS API.
    * **DSN-Vocal (GPT-SoVITS):** Leverage the integrated DSN-Vocal, a GPT-SoVITS-based multi-emotional neural network text-to-speech framework for faster, local text-to-speech processing.
* **API support:** Embed DSN into any application using its API. An example API client is provided in `/examples/api_client.py`.

## Get Started Now:

You can download the packaged Python runtime from [here](https://github.com/ccjjfdyqlhy/DSN-pre/releases), or you can install the dependency libraries yourself.

**1. Prerequisites:**

* **Python 3.11+:** Install Python (3.11.2 recommended) from the [official website](https://www.python.org/).
* **Google Cloud Platform API Key (for online model access):** You can obtain a free trial API key [here](https://aistudio.google.com/app/apikey).
* **Everything Search Engine (for file searching):** Download the full version from their [website](https://www.voidtools.com/downloads) and install it in the `binaries` folder of this cloned repository.
* **Paraformer-zh (for speech recognition):** Download from [Modelscope](https://www.modelscope.cn/models/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch/files) or [HuggingFace](https://huggingface.co/funasr/paraformer-zh) to the `instances\\paraformer` folder.
* **Moondream (for local image recognition):** Download from [HuggingFace](https://huggingface.co/vikhyatk/moondream2) to the `instances\\moondream` folder.
* **Pre-built ChatTTS (another TTS solution):**  Under adaptation, will be supported in the future. 

**2. Installation:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ccjjfdyqlhy/DSN-pre.git
   ```
2. **Install the necessary packages in `install_before_requirements.txt`.**
3. **Download the DSN-local.NT model (optional):**
   * Navigate to the `instances\\DSN` folder within the cloned repository.
   * Download the DSN-local.NT model and place it in the folder.
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Download and configure TTS model resources:**
    * Download the TTS model package from [here](https://github.com/ccjjfdyqlhy/DSN-pre/releases) to the `TTS_models` folder. You can use this folder as a template and use your own trained GPT-SoVITS model for TTS reasoning.
    * Set the model folder path and the model used in `config-ui.py`.

**3. Configuration:**

* **Use the configuration tool to generate `config.py`:**
   ```bash
   python config-ui.py
   ```
   * This will open a user interface where you can adjust various settings for DSN.
   * Once finished, the tool will generate a `config.py` file based on your selections.
* **Further customize settings in `config.py` if necessary:**
    * You can manually edit the `config.py` file to fine-tune settings related to voice control, text-to-speech, visual understanding, local/online models, and more.

**4. Launch DSN:**
* **Run the program:**
   ```bash
   cd DSN-pre
   python DSN.Launch.py
   ```

**Additional Notes:**

* **Note: Before you begin, you must read and agree to all the terms of use in the `LICENSE` file.**
* This project is under active development, and some features may not be fully implemented or may contain bugs. We welcome contributions from the community. 
