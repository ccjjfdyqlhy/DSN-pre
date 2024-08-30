## DSN: Deep Streaming Neural Networks-based Control System Framework

**English** | [简体中文](https://github.com/ccjjfdyqlhy/DSN-pre/blob/main/README_zh-CN.md)  

**DSN** is a powerful and innovative interactive prompting framework that combines the capabilities of large language models and deep learning to create a truly intelligent and engaging conversational experience.   
**This repository is an early preview branch of the project, synced with the main branch on 2024/8/30.**

**DSN can:**

* **Understand and respond to your natural language requests** - You can ask any question, and it will do its best to fulfill your requests.
* **Take full control of your computer** - The framework can automatically execute code or commands on your computer, handling your requests directly.
* **Search for files and information** - Easily find files across your entire disk or search the web for information.
* **Learn from your interactions** - DSN will continuously learn from your interactions and improve its responses over time.
* **Integrate with external applications** - Expand DSN's capabilities using APIs.
* **Support local model deployment** - Use your custom models to run DSN offline.

**Features:**
* **Voice Control:** Talk to DSN and let it hear your commands!
* **Local Model Support:** Use your own custom models for privacy and offline access.
* **Advanced Search Capabilities:** Search for files by name, type, or keywords.
* **Customizable Settings:** Tailor DSN to your needs by adjusting settings in the `config.py` file, which can be easily generated and modified using the `config-ui.py` tool.
* **Customizable Prompts:** Craft your own prompts in the `custom_prompt.py` file to achieve personalized AI effects.
* **Error Handling:** DSN can gracefully handle errors and automatically perform actions like configuring the environment and self-correction.
* **Experience Acceleration:** Recording key points of the conversation in the memo file `memo.txt` can make action execution more efficient and faster.
* **Visual Understanding:** Allow DSN to "see" and analyze images from your camera or local files.
* **Text-to-Speech:** Choose between two TTS solutions:
    * **ChatTTS API:** Access high-quality voices through the local ChatTTS API.
    * **DSN-Vocal (GPT-SoVITS):** Leverage the integrated DSN-Vocal, a multi-emotional neural network text-to-speech framework based on GPT-SoVITS, for faster, local text-to-speech processing. 
* **API Support:** Embed DSN into any application using its API. An API client example is provided in `/examples/api_client.py`. 

## Getting Started:

You can download the build version from [here](), or build it yourself by following these steps:

**1. Prerequisites:**
* **Python 3.11+:** Install Python (3.11.2 recommended) from the [official website](https://www.python.org/).
* **Google Cloud Platform API key (for online model access):** You can obtain a free trial API key [here](https://aistudio.google.com/app/apikey).
* **Everything search engine (for file search):** Download the full version from their [website](https://www.voidtools.com/downloads) and then install it in the "binaries" folder of this cloned repository.

**2. Installation:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ccjjfdyqlhy/DSN-pre.git
   ```
2. **Install the necessary packages in `install_before_requirements.txt`.**

3. **Download the DSN-local.NT model (optional):**
   * Navigate to the `instances\\DSN` folder within the cloned repository.
   * Download the DSN-local.NT model and place it inside the folder. 
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

**3. Configuration:**

* **Use the configuration tool to generate `config.py`:**
   ```bash
   python config-ui.py 
   ```
   * This will open a user interface where you can adjust various settings for DSN.
   * Once finished, the tool will generate the `config.py` file based on your selections.
* **Further customize settings in `config.py` if necessary:**
   * You can manually edit the `config.py` file to fine-tune settings related to voice control, text-to-speech, visual understanding, local/online models, and more.

**4. Launching DSN:**
* **Run the program:**
   ```bash
   cd DSN-pre
   python DSN.Launch.py
   ```

**Additional Notes:**

* **Note: You must read and agree to all terms of use in the `LICENCE` file before starting to use it.**
* This project is under active development, and some features have not yet been fully implemented or are bug-ridden. Community bug fixes are welcome. 
