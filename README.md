## DSN: Deep Streaming Neural Networks-based Control System Framework

**English** | [简体中文](https://github.com/ccjjfdyqlhy/DSN-pre/blob/main/README_zh-CN.md)  

**DSN** is a powerful and innovative interactive prompting framework that combines the power of large language models and deep learning to create truly intelligent and engaging conversational experiences. 
**This repository is currently an early preview branch of the project and will be synced with the core branch on 2024/8/30.**

**DSN can:**

* **Understand and respond to your natural language requests** - You can ask anything, and it will try its best to fulfill your requests.
* **Take full control of your computer** - The framework can automatically execute code or commands on your computer, directly handling your requests.
* **Search for files and information** - Easily find files across your entire disk or search the web for information.
* **Learn from your interactions** - DSN will continuously learn from your interactions, improving its responses over time.
* **Integrate with external applications** - Use APIs to extend DSN's functionalities.
* **Support local model deployment** - Use your own custom models to run DSN offline.

**Features:**  
* **Voice control:** Talk to DSN and let it hear your commands!
* **Local model support:** Use your own custom models for privacy and offline access.
* **Advanced search capabilities:** Search for files by name, type, or keywords.
* **Customizable settings:** Tailor DSN to your needs by adjusting settings in the `config.py` file, which can be easily generated and modified using the `config-ui.py` tool.
* **Customizable prompt words:** You can edit your own prompt words in the `custom_prompt.py` file to achieve personalized AI effects.
* **Error handling:** DSN can gracefully handle errors and automatically perform tasks like configuring environments and self-correction.
* **Experience acceleration:** Recording the key points of the conversation in the memo file `memo.txt` can make action execution more efficient and faster.
* **Visual understanding:** Allow DSN to "see" and analyze images from your camera or local files.
* **Text-to-speech:** Choose between two TTS solutions:
    * **ChatTTS API:** Access high-quality voices through the local ChatTTS API.
    * **DSN-Vocal (GPT-SoVITS):** Leverage the integrated DSN-Vocal, a GPT-SoVITS-based multi-emotional neural network text-to-speech framework for faster, local text-to-speech processing.
* **API support:** Embed DSN into any application using its API. An example API client is provided in `/examples/api_client.py`.

## Get Started Now:

You can download the packaged Python runtime from [here](https://github.com/ccjjfdyqlhy/DSN-pre/releases), or you can install the dependency library yourself.

**1. Prerequisites:**  
* **Python 3.11+:** Install Python from the [official website](https://www.python.org/) (3.11.2 recommended).
* **Google Cloud Platform API key (for online model access):** You can obtain a free trial API key [here](https://aistudio.google.com/app/apikey).
* **Everything search engine (for file searching):** Download the full version from their [website](https://www.voidtools.com/downloads), then install it in the "binaries" folder of this cloned repository.

**2. Installation:**

1. **Clone the repository:** 
   ```bash
   git clone https://github.com/ccjjfdyqlhy/DSN-pre.git
   ```
2. **Install the necessary packages in `install_before_requirements.txt`.**

3. **Download the DSN-local.NT model (optional):**
   * Navigate to the `instances\\DSN` folder in the cloned repository.
   * Download the DSN-local.NT model and place it in the folder.
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Download and configure TTS model resources:**
   * Download the TTS model package from [here]() to the `TTS_models` folder. You can use this folder as a template and use your own trained GPT-SoVITS model for TTS inference.
   * Set the used model folder path and the used model in `config-ui.py`. 

**3. Configuration:**

* **Generate `config.py` using the configuration tool:**
   ```bash
   python config-ui.py 
   ```
   * This will open a user interface where you can adjust various settings for DSN.
   * Upon completion, the tool will generate the `config.py` file based on your selections.
* **Further customize settings in `config.py` if necessary:**
    * You can manually edit the `config.py` file to fine-tune settings related to voice control, text-to-speech, visual understanding, local/online models, etc.

**4. Launch DSN:**
* **Run the program:**
   ```bash
   cd DSN-pre
   python DSN.Launch.py
   ```

**Additional Notes:**

* **Attention: You must read and agree to all terms of use in the `LICENCE` file before you start using it.**
* This project is under active development, and some features may not be fully implemented or may have bugs. We welcome bug reports from the community. 
