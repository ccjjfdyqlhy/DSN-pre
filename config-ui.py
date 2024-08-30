from nicegui import ui, app
import os
cwd = os.getcwd()
# 配置文件路径
config_file = cwd+'\\config.py'

# 定义默认值
defaults = {
    "DEBUG": False,
    "PAUSE": False,
    "PYTHON": "<运行时Python路径>",
    "TTS_PYTHON": "<TTS Python路径>",
    "MULTI_PROCESSING": False,
    "THREAD": 4,
    "USE_LOCAL": False,
    "MODEL_PATH": r"<本地DSN模型路径.NT>",
    "GPU_LAYERS": 44,
    "CONTEXT_WINDOW": 10000,
    "LOCAL_SEED": 0,
    "MOONDREAM_PATH": r"<Moondream路径>",
    "PARAFORMER_PATH": r"<Paraformer路径>",
    "CHATTTS_PATH": r"<ChatTTS路径>",
    "DSNVOCAL_PATH": r"<DSN-vocal路径>",
    "GENAI_APIKEY": "<您的API密钥>",
    "GENAI_TRANSPORT_TYPE": "rest",
    "SELECTED_MODEL": "gemini-1.0-pro-latest",
    "CITY": "<您的城市>",
    "TIMEZONE": "<您的时区>",
    "BROWSER": "Edge",
    "USER_PYTHON": r"<您的首选Python路径>",
    "AI_NAME": "<AI名称>",
    "LANG": "中英混合",
    "AI_CHARACTER": "",
    "AI_CHARACTER_SOURCE": "",
    "USE_CUSTOM_PROMPT": False,
    "USE_LITE_PROMPT": False,
    "USE_MEMO": True,
    "LAYERS_LIMIT": 20,
    "ENABLE_PLUGINS": False,
    "ALLOW_VISION": True,
    "USE_ONLINE_VISION": True,
    "USE_BACKUP_VISION": True,
    "AUTO_VISION": False,
    "USE_CAMERA": "False",  # 'True', 'False', 或 'Auto'
    "SPEECH_CONTROL": False,
    "PF_BTSIZE": 300,
    "EXCEED_TIME": 600,
    "TEXT_TO_SPEECH": False,
    "TTS_MODEL_NAME": "<模型名称>",
    "TTS_MODEL_PATH": r"<TTS模型包路径>",
    "USE_CHATTTS": True,
    "CHATTTS_SEED": 0,
    "CHATTTS_TEMP": 0.3,
    "USERNAME": "<您的用户名>" # 添加用户名字配置项
}

# 定义可能包含路径的配置项
path_keys = [
    "PYTHON", "TTS_PYTHON", "MODEL_PATH", "MOONDREAM_PATH",
    "PARAFORMER_PATH", "CHATTTS_PATH", "DSNVOCAL_PATH",
    "PYTHON", "TTS_PYTHON", "MODEL_PATH", "MOONDREAM_PATH",
    "PARAFORMER_PATH", "CHATTTS_PATH", "DSNVOCAL_PATH",
    "USER_PYTHON", "TTS_MODEL_PATH"
]

# 从配置文件加载设置
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    try:
                        # 尝试将值转换为字符串以外的类型
                        defaults[key] = eval(value)
                    except:
                        # 如果转换失败，则保留为字符串
                        defaults[key] = value

# 将配置保存到文件
def save_config():
    with open(config_file, 'w', encoding='utf-8') as f:
        for key, value in defaults.items():
            if isinstance(value, str):
                if key in path_keys:
                    f.write(f'{key} = r"{value}"\n')
                else:
                    f.write(f'{key} = "{value}"\n')
            else:
                f.write(f'{key} = {value}\n')

def save_config_and_quit():
    save_config()
    ui.run_javascript('window.close()')
    app.shutdown()

# UI界面函数
def create_ui():
    ui.label("切记：使用底部按钮关闭该界面")
    with ui.row():
        with ui.column():
            with ui.card().style('width: 300px'):
                ui.label("运行时").classes('text-h5')
                with ui.row():
                    ui.input(label="Python可执行文件", placeholder=defaults["PYTHON"], value=defaults.get("PYTHON")).props(
                        "outline")
                with ui.row():
                    ui.input(label="TTS Python可执行文件", placeholder=defaults["TTS_PYTHON"],
                             value=defaults.get("TTS_PYTHON")).props("outline")
                with ui.row():
                    ui.checkbox("调试模式", value=defaults["DEBUG"]).bind_value(defaults, "DEBUG")
                    ui.checkbox("暂停模式", value=defaults["PAUSE"]).bind_value(defaults, "PAUSE")

            with ui.card().style('width: 300px'):
                ui.label("启动").classes('text-h5')
                ui.checkbox("多进程", value=defaults["MULTI_PROCESSING"]).bind_value(defaults, "MULTI_PROCESSING")
                # 修改number组件宽度
                ui.number(label="线程数", value=defaults["THREAD"], step=1, min=1).bind_value(defaults, "THREAD").style('width: 200px')


            with ui.card().style('width: 300px'):
                ui.label("本地模型").classes('text-h5')
                ui.checkbox("使用本地模型", value=defaults["USE_LOCAL"]).bind_value(defaults, "USE_LOCAL")
                ui.input(label="模型路径", placeholder=defaults["MODEL_PATH"]).bind_value(defaults, "MODEL_PATH").props(
                    "outline")
                # 修改GPU层数组件宽度
                ui.number(label="GPU层数（最大44）", value=defaults["GPU_LAYERS"], step=1, min=1, max=44).bind_value(
                    defaults, "GPU_LAYERS").style('width: 200px')
                # 修改GPU层数组件宽度
                ui.number(label="GPU层数（最大44）", value=defaults["GPU_LAYERS"], step=1, min=1, max=44).bind_value(
                    defaults, "GPU_LAYERS").style('width: 200px')
                ui.number(label="上下文窗口", value=defaults["CONTEXT_WINDOW"], step=100).bind_value(defaults,
                                                                                                 "CONTEXT_WINDOW")
                ui.number(label="本地种子", value=defaults["LOCAL_SEED"]).bind_value(defaults, "LOCAL_SEED")

        with ui.column():
            with ui.card().style('width: 300px'):
                ui.label("实例").classes('text-h5')
                ui.input(label="Moondream路径", placeholder=defaults["MOONDREAM_PATH"]).bind_value(defaults,
                                                                                                 "MOONDREAM_PATH").props(
                    "outline")
                ui.input(label="Paraformer路径", placeholder=defaults["PARAFORMER_PATH"]).bind_value(defaults,
                                                                                                   "PARAFORMER_PATH").props(
                    "outline")
                ui.input(label="ChatTTS路径", placeholder=defaults["CHATTTS_PATH"]).bind_value(defaults,
                                                                                                 "CHATTTS_PATH").props(
                    "outline")
                ui.input(label="DSN-Vocal路径", placeholder=defaults["DSNVOCAL_PATH"]).bind_value(defaults,
                                                                                                 "DSNVOCAL_PATH").props(
                    "outline")

            with ui.card().style('width: 300px'):
                ui.label("GenAI API").classes('text-h5')
                ui.input(label="API密钥", placeholder=defaults["GENAI_APIKEY"]).bind_value(defaults,
                                                                                             "GENAI_APIKEY").props(
                    "password")
                ui.select(options=["rest", "grpc"], label="传输类型", value=defaults["GENAI_TRANSPORT_TYPE"]).bind_value(
                    defaults, "GENAI_TRANSPORT_TYPE").style('width: 200px')
                ui.input(label="选择的模型", placeholder=defaults["SELECTED_MODEL"]).bind_value(defaults,
                                                                                                 "SELECTED_MODEL").props(
                    "outline")

            with ui.card().style('width: 300px'):
                ui.label("语音控制").classes('text-h5')
                ui.checkbox("语音控制", value=defaults["SPEECH_CONTROL"]).bind_value(defaults, "SPEECH_CONTROL")
                ui.number(label="语音识别BATCH_SIZE", value=defaults["PF_BTSIZE"], step=10).bind_value(defaults,
                                                                                                     "PF_BTSIZE").style(
                    'width: 200px')
                ui.number(label="最大语音时间（单位）", value=defaults["EXCEED_TIME"], step=10).bind_value(defaults,
                                                                                                     "EXCEED_TIME").style(
                    'width: 200px')


        with ui.column():
            with ui.card().style('width: 300px'):
                ui.label("AI设置").classes('text-h5')
                ui.input(label="AI名称", placeholder=defaults["AI_NAME"]).bind_value(defaults, "AI_NAME").props("outline")
                # 修改AI语言选项
                ui.select(options=["中英混合", "English"], label="AI语言", value=defaults["LANG"]).bind_value(defaults,
                                                                                                      "LANG")
                ui.input(label="角色参考（名称）", placeholder=defaults["AI_CHARACTER"]).bind_value(defaults,
                                                                                                   "AI_CHARACTER").props(
                    "outline")
                ui.input(label="角色参考（来源）", placeholder=defaults["AI_CHARACTER_SOURCE"]).bind_value(defaults,
                                                                                                     "AI_CHARACTER_SOURCE").props(
                    "outline")
                ui.checkbox("使用自定义提示", value=defaults["USE_CUSTOM_PROMPT"]).bind_value(defaults,
                                                                                            "USE_CUSTOM_PROMPT")
                ui.checkbox("使用精简提示", value=defaults["USE_LITE_PROMPT"]).bind_value(defaults, "USE_LITE_PROMPT")
                ui.checkbox("启用「备忘录」", value=defaults["USE_MEMO"]).bind_value(defaults, "USE_MEMO")
                ui.number(label="自纠错层数限制", value=defaults["LAYERS_LIMIT"], step=1, min=1).bind_value(defaults,
                                                                                                 "LAYERS_LIMIT")

            with ui.card().style('width: 300px'):
                ui.label("多模态设置").classes('text-h5')
                ui.checkbox("启用插件", value=defaults["ENABLE_PLUGINS"]).bind_value(defaults, "ENABLE_PLUGINS")
                ui.checkbox("允许视觉", value=defaults["ALLOW_VISION"]).bind_value(defaults, "ALLOW_VISION")
                ui.checkbox("使用API视觉", value=defaults["USE_ONLINE_VISION"]).bind_value(defaults, "USE_ONLINE_VISION")
                ui.checkbox("预加载本地视觉", value=defaults["USE_BACKUP_VISION"]).bind_value(defaults, "USE_BACKUP_VISION")
                ui.checkbox("自动视觉", value=defaults["AUTO_VISION"]).bind_value(defaults, "AUTO_VISION")
                ui.select(options=["True", "False", "Auto"], label="使用相机", value=defaults["USE_CAMERA"]).bind_value(
                    defaults, "USE_CAMERA").style('width: 200px')

        with ui.column():
            with ui.card().style('width: 300px'):
                ui.label("文本转语音").classes('text-h5')
                ui.checkbox("文本转语音", value=defaults["TEXT_TO_SPEECH"]).bind_value(defaults, "TEXT_TO_SPEECH")
                ui.input(label="TTS模型名称", placeholder=defaults["TTS_MODEL_NAME"]).bind_value(defaults,
                                                                                                 "TTS_MODEL_NAME").props(
                    "outline")
                ui.input(label="TTS模型路径", placeholder=defaults["TTS_MODEL_PATH"]).bind_value(defaults,
                                                                                                 "TTS_MODEL_PATH").props(
                    "outline")
                ui.checkbox("使用ChatTTS", value=defaults["USE_CHATTTS"]).bind_value(defaults, "USE_CHATTTS")
                ui.number(label="ChatTTS种子", value=defaults["CHATTTS_SEED"]).bind_value(defaults, "CHATTTS_SEED")
                ui.number(label="ChatTTS温度", value=defaults["CHATTTS_TEMP"], step=0.1, min=0,
                          max=1).bind_value(defaults,
                                          "CHATTTS_TEMP").style('width: 200px')
            with ui.card().style('width: 300px'):
                ui.label("用户资料").classes('text-h5')
                ui.input(label="用户名字", placeholder=defaults["USERNAME"]).bind_value(defaults, "USERNAME").props(
                    "outline")

                ui.input(label="城市", placeholder=defaults["CITY"]).bind_value(defaults, "CITY").props("outline")
                ui.input(label="时区（UTC）", placeholder=defaults["TIMEZONE"]).bind_value(defaults, "TIMEZONE").props(
                    "outline")
                ui.select(options=["Chrome", "Edge", "Firefox"], label="浏览器", value=defaults["BROWSER"]).bind_value(
                    defaults, "BROWSER").style('width: 200px')
                ui.input(label="首选Python路径", placeholder=defaults["USER_PYTHON"]).bind_value(defaults,
                                                                                                   "USER_PYTHON").props(
                    "outline")
# 在底部添加保存/加载按钮
    with ui.row():
        ui.button("保存并关闭", on_click=save_config_and_quit)


# 加载默认配置
load_config()
# 创建UI界面
create_ui()

ui.run(title='DSN config UI',reload=False)