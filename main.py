
# DSN main
# update 240830

from utils import *


play_audio = False # Filter API reference
ver = 'Rev2_0.9.8'
BUILDNUM = 240830
cwd = os.getcwd()
platform = sys.platform
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
use_device = 'camera'
building = False
skip_wait = False
global result
splits = ["，", "。", "？", "！", ",", ".", "?", "!", "~", ":", "：", "—", "…"]


def send(chat=None,msgcontent='') -> str:
    if USE_LOCAL:
        output = llm.create_chat_completion(messages=msgcontent)
        history.append({"role": "assistant", "content": output})
        return extract_model_output(str(output))
    else:
        return chat.send_message(msgcontent,safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }).text

def decrypt(prompt):
    return llm.detokenize(prompt).decode('utf-8')

def get_voice(refer_wav,refer_text,prompt_language,text):
    headers = {'Content-Type': 'application/json'}
    data = {
        "refer_wav_path": refer_wav,
        "prompt_text": refer_text,
        "prompt_language": prompt_language,
        "text": text,
        "text_language": "zh"
    }
    response = requests.post('http://127.0.0.1:3826', headers=headers, json=data)
    if response.status_code == 200:
        wav_data = response.content
        with open(cwd+'\\TEMP\\latest_generated.wav', 'wb') as f:
            f.write(wav_data)
        if play_audio:
            CHUNK=1024;wf=wave.open(cwd+'\\TEMP\\latest_generated.wav','rb');wav_data=wf.readframes(CHUNK);p = pyaudio.PyAudio();FORMAT=p.get_format_from_width(wf.getsampwidth());CHANNELS=wf.getnchannels();RATE=wf.getframerate();stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,frames_per_buffer=CHUNK,output=True)
            while len(wav_data) > 0:
                stream.write(wav_data)
                wav_data = wf.readframes(CHUNK)
    else:
        print(response)

def get_vision(use_file=False,file_route='',prompt=''):
    if USE_ONLINE_VISION:
        try:
            return get_vision_online(use_file,file_route,prompt)
        except Exception as e:
            print(e)
            print('[ 使用本地图片识别 ]')
    if use_file:
        if file_route == '':
            image_path = input('[ 键入图片路径 ] > ')
            print('使用本地图片：'+image_path)
        else:
            image_path = file_route
    else:
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        ret, frame = cap.read()
        cv2.imwrite(cwd+'\\TEMP\\latest_photo.jpg', frame)
        print('[ 拍照成功 ]')
        cap.release()
        image_path = cwd+'\\TEMP\\latest_photo.jpg'
    try:
        image = Image.open(image_path)
        enc_image = picmodel.encode_image(image)
        vision_ans=(picmodel.answer_question(enc_image, "Describe this image.", tokenizer))
    except FileNotFoundError:
        print('[ 文件不存在 ]')
    return vision_ans

def transcribe(path):
    res = s2tmodel.generate(input=path,batch_size_s=PF_BTSIZE)
    for dic in res:
        for key, value in dic.items():
            if key == 'text':
                result = value.replace(' ', '')
    return result

def save_history(api_tag=False):
    folder = cwd+"\\generated\\chat_history"
    if not os.path.exists(folder):
        os.makedirs(folder)
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if USE_LOCAL:
        history_file_path = os.path.join(folder, f"[LOCAL]history{time_str}.txt")
        if len(history) > 0:
            with open(history_file_path, "w", encoding="utf-8") as f:
                for message in history:
                    f.write(message)
                    f.write("\n")
                f.close()
    else:
        if agent_id != 0:
            history_file_path = os.path.join(folder, f"[AGENT{agent_id}]history{time_str}.txt")
        elif api_tag:
            history_file_path = os.path.join(folder, f"[API]history{time_str}.txt")
        else:
            history_file_path = os.path.join(folder, f"history{time_str}.txt")
        if len(chat.history) > 0:
            with open(history_file_path, "w", encoding="utf-8") as f:
                for message in chat.history:
                    f.write(f'{message.role}: {message.parts[0].text}')
                    f.write("\n")
                f.close()
    print(f"\n聊天记录已保存到文件： {history_file_path}")

# 将原 merge_msg 函数中需要用户交互的部分移到主循环
def xpost(msgin, use_device, building):
    return_vision = False
    if AUTO_VISION:
        for keyword in VISION_KEYWORDS:
            if keyword in msgin:
                return_vision = True
                if USE_CAMERA == 'True':
                    use_device = 'camera'
                    pic_msg = VISION_START1+get_vision(False)
                elif USE_CAMERA == 'False':
                    use_device = 'image'
                    pic_msg = VISION_START2+get_vision(True)
                elif USE_CAMERA == 'Auto':
                    for keyword in CAMERA_KEYWORDS:
                        if keyword in msgin:
                            use_device = 'camera'
                            pic_msg = VISION_START1+get_vision(False)
                        break
                    for keyword in IMAGE_KEYWORDS:
                        if keyword in msgin:
                            use_device = 'image'
                            pic_msg = VISION_START2+get_vision(True)
                        break
                    #TEMP = 'cam'
                    #TEMP = input('[早期未实现功能的替代品] 选择使用摄像头还是本地图片(cam/img)> ')
                    #if TEMP == 'cam':
                    #    use_device = 'camera'
                    #    pic_msg = VISION_START1+get_vision(False)
                    #elif TEMP == 'img':
                    #    use_device = 'image'
                    #    pic_msg = VISION_START2+get_vision(True)
                break
    else:
        TEMP,route = beautify(msgin)
        if 'VISION' in msgin or '使用视觉' in msgin:
            return_vision = True
            if USE_CAMERA == 'True':
                use_device = 'camera'
                pic_msg = VISION_START1+get_vision(False)
            elif USE_CAMERA == 'False':
                use_device = 'image'
                pic_msg = VISION_START2+get_vision(True)
            else:
                return_vision = False
                print('[ 配置文件冲突：USE_CAMERA在未开启AUTO_VISION时只能为True或False，跳过应用视觉。 ]')
        else:
            for item in route:
                if '.jpg' in item or '.png' in item or '.jpeg' in item or '.bmp' in item:
                    print('[ 图片已上传 ]')
                    return_vision = True
                    use_device = 'image'
                    pic_msg = VISION_START2+get_vision(True,item)
    if msgin == 'BUILD_TRAIN_DATA' or msgin == '构建加速模型':
        building = True
        return '请你阅读'+cwd+'\\generated\\chat_history\\文件夹下的全部内容。'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if return_vision:
        msg = "系统UTC+8时间："+timestamp+" "+pic_msg+" 用户输入："+msgin
    else:
        msg = "系统UTC+8时间："+timestamp+" 用户输入："+msgin
    return msg, use_device, building

def handle_output(output,execute_layer=1):
    if output.startswith('cmd /c'):
        result = str(os.popen(output+' 2>&1').readlines())
        if DEBUG: print(result)
        if DEBUG: print('[ 系统指令已执行 ]')
        skipreturn = False
    elif output.startswith('```python'):
        folder = cwd+"\\generated\\program_history"
        if not os.path.exists(folder):
            os.makedirs(folder)
        time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        history_file_path = os.path.join(folder, f"program{time_str}.py")
        code_content = extract_code(output)
        with open(history_file_path, "w", encoding="utf-8") as f:
            f.write(code_content)
            f.close()
        if not os.path.exists('TEMP'):
            os.makedirs('TEMP')
        with open(cwd+'\\TEMP\\historydest.txt','w',encoding='utf-8') as f:
            f.write(history_file_path)
            f.close()
        coderunner = subprocess.Popen([PYTHON, cwd+'\\coderunner.py'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = coderunner.communicate()[0].decode('gbk')
        if DEBUG:print(result)
        if DEBUG: print('[ Python代码已运行 ]')
        skipreturn = False
    elif '[GETDAILYINFO]' in output:
        result = str(get_dailyinfo())
        if DEBUG: print('[ 获取今日信息 ]')
        skipreturn = False
    elif output.startswith('[SFBYNAME]'):
        process = output.split(' ')
        if DEBUG: print('[ 以标准文件名为索引检索：'+process[1]+' ]')
        result = str(search_file_by_name(process[1]))
        if DEBUG:print(result)
        if DEBUG:print('[ 检索完成 ]')
        skipreturn = False
    elif output.startswith('[SFBYKIND]'):
        process = output.split(' ')
        if DEBUG: print('[ 以文件类型为索引检索：'+process[1]+', Keyword: '+process[2]+' ]')
        result = str(search_file_by_kind(process[1], process[2]))
        if DEBUG:print(result)
        if DEBUG:print('[ 检索完成 ]')
        skipreturn = False
    elif output.startswith('[SFBYKEY]'):
        process = output.split(' ')
        if DEBUG: print('[ 以关键词模糊检索：'+process[1]+' ]')
        result = str(search_file_by_keyword(process[1]))
        if DEBUG:print(result)
        if DEBUG:print('[ 检索完成 ]')
        skipreturn = False
    elif output == '[VISION]':
        if AUTO_VISION:
            if USE_CAMERA == 'True':
                print('[正在使用摄像头]')
                result = get_vision(False)
            elif USE_CAMERA == 'False':
                result = get_vision(True)
            elif USE_CAMERA == 'Auto':
                if use_device == 'camera':
                    print('[正在使用摄像头]')
                    result = get_vision(False)
                elif use_device == 'image':
                    result = get_vision(True)
        else:
            result = '用户禁止你使用视觉。'
        skipreturn = False
    elif output.startswith('[IMG]'):
        process = output.split(' ')
        print('[ 分析图片：'+process[1]+' ]')
        try:
            result = get_vision(True,file_route=process[1],prompt=process[2])
        except IndexError:
            result = get_vision(True,file_route=process[1])
        skipreturn = False
    elif '[SAVE_HISTORY]' in output:
        save_history()
        print('[ 聊天记录已存档 ]')
        result = ''
        skipreturn = False
    elif output.startswith('[END_CONVERSATION]'):
        print('['+AI_NAME+' 结束了对话。]')
        print("重新启动程序以继续。")
        return False
    else:
        if TEXT_TO_SPEECH:
            output, filepaths = beautify(output)
            if DEBUG: print(filepaths)
            current_line = 1
            for line in [x for x in output.split('\n') if x]:
                print('[ 段落 '+str(current_line)+' ]')
                if line != '' and line != '\n':
                    if line.endswith('。'):
                        linelength = len(line.split('。'))-1
                    else:
                        linelength = len(line.split('。'))
                    if DEBUG: print(line.split('。'))
                    else: print('[ 构建回答... 总数：'+str(linelength)+' ]')
                    current_sentence = 1
                    for sentence in line.split('。'):
                        if sentence != '' and sentence != '\n':
                                if USE_CHATTTS:
                                    chattts(sentence)
                                else:
                                    if LANG == '中英混合':
                                        if TTS_MODEL_NAME == 'Venti-EN':
                                            get_voice(
                                                refer_wav=TTS_MODEL_PATH+r"/audios/Venti/test.wav",#TODO
                                                refer_text="Many people may feel lost at times. After all, it's impossible for everything to happen according to your own wishes.",
                                                prompt_language='en',
                                                text=sentence,
                                            )
                                        elif TTS_MODEL_NAME == 'Venti-CN':
                                            get_voice(
                                                refer_wav=TTS_MODEL_PATH+r"/audios/emotion_templates/#calm2.wav",#TODO
                                                refer_text="蒲公英子就像自然的宝石，汇聚着每年第一缕风。人们把它放进酒桶，就是把当下的风放了进去。",
                                                prompt_language='zh',
                                                text=sentence,
                                            )
                                        elif TTS_MODEL_NAME == '温迪':
                                            get_voice(
                                                refer_wav=TTS_MODEL_PATH+r"/audios/emotion_templates/#calm2.wav",#TODO
                                                refer_text="蒲公英子就像自然的宝石，汇聚着每年第一缕风。人们把它放进酒桶，就是把当下的风放了进去。",
                                                prompt_language='zh',
                                                text=sentence,
                                            )
                                    elif LANG == 'English':
                                        get_voice(
                                            refer_wav=TTS_MODEL_PATH+r"/audios/Venti/test.wav",#TODO
                                            refer_text="Many people may feel lost at times. After all, it's impossible for everything to happen according to your own wishes.",
                                            prompt_language='en',
                                            text=sentence,
                                        )
                                    else:
                                        print('[ TTS Language not supported. ]')
                                    print(' ['+str(current_sentence)+'/'+str(linelength)+'] '+sentence)
                                    for item in filepaths:
                                        print('< '+item)
                                    filepaths = []
                                    current_sentence += 1
                current_line += 1
        else:
            print('< '+output)
        result=''
        skipreturn = True
    if skipreturn == False:
        if str(result) == '' or result == '[]':
            response = send(chat,'[控制系统返回] 操作成功完成。')
            print('[ 第 '+str(execute_layer)+' 层动作完成 ]')
        else:
            if execute_layer >= 10 and execute_layer <= LAYERS_LIMIT:
                print('[ 第 '+str(execute_layer)+' 层动作完成 / 自纠错限制: '+LAYERS_LIMIT+'层 ]')
                execute_layer = execute_layer + 1
                response = send(chat,'[控制系统返回] '+str(result))
                handle_output(response, execute_layer)
            elif execute_layer > LAYERS_LIMIT:
                print('[ 第 '+str(execute_layer)+' 层动作完成 / 达到最大纠错层数 ]')
                response = send(chat,'停止尝试纠正，错误次数太多。请详细描述遇到的错误，以便我们一起解决它。')
                print('< '+response)
            else:
                print('[ 第 '+str(execute_layer)+' 层动作完成 ]')
                execute_layer = execute_layer + 1
                response = send(chat,'[控制系统返回] '+str(result))
                handle_output(response, execute_layer)

def init(silent=False):
    '''
    初始化控制系统。
    执行该操作将会连接所有节点的控制流，并部署每个节点上的生成式模型。
    
    Args:
        silent (bool): 是否以静默模式（仅输出问题）运行。默认为 False。
    '''
    global llm, history, chat, picmodel, tokenizer, agent_id, s2tmodel, PROMPT
    from prompt import STATUS, VISION_START1, VISION_START2, MAIN_PROMPT, PROMPT_LITE, BEGINNING_PROMPT, COMMAND_PROMPT, SEARCH_LOCAL_PROMPT, SEARCH_ONLINE_PROMPT, READ_FILE_PROMPT, VISION_PROMPT, p_PROTECT, p_MEMO, p_PLUGINS, p_ENDING
    from config import DEBUG, USE_LOCAL, MODEL_PATH, GPU_LAYERS, CONTEXT_WINDOW, LOCAL_SEED, MOONDREAM_PATH, PARAFORMER_PATH, GENAI_APIKEY, GENAI_TRANSPORT_TYPE, SELECTED_MODEL, USE_CUSTOM_PROMPT, USE_LITE_PROMPT, USE_MEMO, ENABLE_PLUGINS, ALLOW_VISION, USE_ONLINE_VISION, USE_BACKUP_VISION, AUTO_VISION, USE_CAMERA, SPEECH_CONTROL, TEXT_TO_SPEECH, USE_CHATTTS
    if not check_process('Everything.exe'):
        print('搜索服务未运行，正在启动。\n')
        start_everything()
    if USE_LOCAL:
        if silent == False: print('正在初始化本地模型...')
        try:
            if LOCAL_SEED == 0:
                llm = Llama(
                    model_path=MODEL_PATH,
                    n_gpu_layers=GPU_LAYERS,
                    n_ctx=CONTEXT_WINDOW
                )
            else:
                llm = Llama(
                    model_path=MODEL_PATH,
                    n_gpu_layers=GPU_LAYERS,
                    n_ctx=CONTEXT_WINDOW,
                    seed = LOCAL_SEED
                )
            if sys.platform == 'win32':
                os.system('cls')
            elif sys.platform == 'linux':
                os.system('clear')
        except:
            print('本地模型初始化失败。请确保已经正确在'+cwd+'\\instances文件夹下安装了DSN-local.NT模型，python环境正常，以及配置文件无误。')
            exit()
        if silent == False: print('本地部署完成。模型已就绪。')
    else:
        llm = None
    try:
        genai.configure(api_key=GENAI_APIKEY,transport=GENAI_TRANSPORT_TYPE)
    except:
        print('API初始化失败。请确保已经正确配置了API密钥。')
        exit()
    model = genai.GenerativeModel(model_name=SELECTED_MODEL)
    history = []
    chat = model.start_chat(history=history)
    if silent == False: print('API初始化完成。')
    if type(VISION_START1) == list:
        VISION_START1 = decrypt(VISION_START1)
        VISION_START2 = decrypt(VISION_START2)
        if USE_CUSTOM_PROMPT:
            from custom_prompt import CUSTOM_PROMPT
            PROMPT = decrypt(BEGINNING_PROMPT)+CUSTOM_PROMPT
        else:
            if USE_LITE_PROMPT:
                PROMPT = decrypt(PROMPT_LITE)
            else:
                if ENABLE_PLUGINS:
                    PROMPT=STATUS+decrypt(MAIN_PROMPT)+decrypt(COMMAND_PROMPT)+decrypt(SEARCH_LOCAL_PROMPT)+decrypt(SEARCH_ONLINE_PROMPT)+decrypt(READ_FILE_PROMPT)+decrypt(VISION_PROMPT)+decrypt(p_PROTECT)+decrypt(p_PLUGINS)
                else:
                    PROMPT=STATUS+decrypt(MAIN_PROMPT)+decrypt(COMMAND_PROMPT)+decrypt(SEARCH_LOCAL_PROMPT)+decrypt(SEARCH_ONLINE_PROMPT)+decrypt(READ_FILE_PROMPT)+decrypt(VISION_PROMPT)+decrypt(p_PROTECT)+decrypt(p_ENDING)
    else:
        if USE_CUSTOM_PROMPT:
            from custom_prompt import CUSTOM_PROMPT
            PROMPT = BEGINNING_PROMPT+CUSTOM_PROMPT
        else:
            if USE_LITE_PROMPT:
                PROMPT = PROMPT_LITE
            else:
                if ENABLE_PLUGINS:
                    PROMPT=STATUS+MAIN_PROMPT+COMMAND_PROMPT+SEARCH_LOCAL_PROMPT+SEARCH_ONLINE_PROMPT+READ_FILE_PROMPT+VISION_PROMPT+p_PROTECT+p_PLUGINS
                else:
                    PROMPT=STATUS+MAIN_PROMPT+COMMAND_PROMPT+SEARCH_LOCAL_PROMPT+SEARCH_ONLINE_PROMPT+READ_FILE_PROMPT+VISION_PROMPT+p_PROTECT+p_ENDING

    if USE_MEMO:
        if os.path.exists('memo.txt'):
            with open('memo.txt', 'r', encoding='utf-8-sig') as f:
                memo = f.read()
                if silent               == False: print("备忘录已载入。")
        else:
            print("启用了备忘录，但是 memo.txt 不存在，创建新文件。")
            with open('memo.txt', 'w', encoding='utf-8-sig') as f:
                f.write('')    
            memo = ''
        if type(p_MEMO) == list:
            p_MEMO = decrypt(p_MEMO)
        PROMPT = PROMPT+p_MEMO+memo
    history = [{'role': 'user', 'content': PROMPT}]
    if silent == False: print("提示词加载完成。")

    if silent == False: print('\nDeep Streaming Neural Network Interactive Prompt\n核心 Framework 版本 '+ver+' build '+str(BUILDNUM)+'\n')
    try:
        print('实例节点编号: '+sys.argv[1])
        agent_id = int(sys.argv[1])
    except:
        if USE_LOCAL:
            pass
        else:
            print('未采用分布式处理。智能体可能会出现不可预测的行为。')
        agent_id = 0
    print()
    if DEBUG: print('WARNING: Debug 模式已启用。用户体验可能会受到不良影响。')
    if silent == False and ENABLE_PLUGINS: print('加速器加载已启用。加载耗时会更长。\n')
    if TEXT_TO_SPEECH:
        if USE_CHATTTS:
            start_chattts()
        else:
            start_tts()
    if (ALLOW_VISION and not USE_ONLINE_VISION) or (ALLOW_VISION and USE_ONLINE_VISION and USE_BACKUP_VISION):
        skip_wait = True
        if USE_BACKUP_VISION:
            if silent == False: print('正在初始化视觉模型以作为后备解决方案...')
        else:
            if silent == False: print('正在初始化视觉模型...')
        try:
            picmodel = AutoModelForCausalLM.from_pretrained(MOONDREAM_PATH,trust_remote_code=True)
            tokenizer = AutoTokenizer.from_pretrained(MOONDREAM_PATH,trust_remote_code=True)
        except OSError:
            print('视觉模型未找到。请确保已经正确在'+cwd+'\\instances文件夹下安装了Moondream模型，python环境正常，以及配置文件无误。')
            exit()
        if silent == False: print('视觉模型已启用。已准备好处理图像。')
    if SPEECH_CONTROL: 
        if silent == False: print('正在初始化语音控制模型...')
        try:
            s2tmodel = AutoModel(model=PARAFORMER_PATH,disable_update=True)
        except OSError:
            print('语音控制模型未找到。请确保已经正确在'+cwd+'\\instances文件夹下安装了Paraformer模型，python环境正常，以及配置文件无误。')
            exit()
        if silent == False: print('语音控制已启用。试着通过说话命令DSN执行操作！\n')
    if silent == False: print('欲修改设置，请使用 config-ui.py。')
    if silent == False: print('可供合成经验加速模型的迭代次数: '+str(len(os.listdir(cwd+'\\generated\\chat_history\\'))))
    if TEXT_TO_SPEECH and not USE_CHATTTS:
        if not skip_wait:
            if silent == False: print('等待TTS初始化...(10s)')
            time.sleep(10)
    if ALLOW_VISION:
        if AUTO_VISION:
            if silent == False: print('自动视觉已启用。AI会学习你的上下文来决定是否需要通过摄像头获取视觉。')
            if USE_CAMERA == False:
                print('USE_CAMERA设置项已强制覆盖为自动。')
            USE_CAMERA = 'Auto'
        else:
            if SPEECH_CONTROL:
                print('自动视觉已禁用。在你的句子中提到“使用视觉”来让AI处理图像。')
            else:
                if silent == False: print('在你的输入中加入 VISION 来让AI处理图片。')
    if USE_CUSTOM_PROMPT:
        if PROMPT != '':
            if silent == False: print('自定义提示词已启用。')
        else:
            print('自定义提示提示词为空。这将对AI没有自定义效果。转到 custom_prompt.py 修改。')
    if SPEECH_CONTROL:
        if silent == False: print('说出“构建加速模型”来立即采用本次聊天记录合成经验加速模型。')
    else:
        if silent == False: print('使用指令 BUILD_TRAIN_DATA 来立即采用本次聊天记录合成经验加速模型。')
    if SPEECH_CONTROL:
        if silent == False: print('说出“结束对话”来让AI保存聊天记录并结束对话。')
    else:
        if silent == False: print('使用 Ctrl+C 组合键来以结束。')
    print()
    try:
        if not os.path.exists(cwd+'\\TEMP\\'):
            os.makedirs(cwd+'\\TEMP\\')
        with open(cwd+'\\TEMP\\last_login.txt', 'r') as f: last_login = f.read(); f.close()
    except FileNotFoundError: last_login = 'Never'; f = open(cwd+'\\TEMP\\last_login.txt', 'w'); f.close()
    if silent == False and USE_LOCAL: print('WARNING: 目前本地模型的动作执行能力很差，有时无法完成一个动作，之后会改进。建议使用在线模型已获得更好的体验。')
    print('上次登录：'+last_login+'\n')
    with open(cwd+'\\TEMP\\last_login.txt', 'w') as f: f.write(timestamp); f.close()
    
    try:
        # 将原本在主循环中的初始化逻辑移动到init函数
        if ENABLE_PLUGINS:
            print('[配置加速器](1/3) < '+send(chat,PROMPT+'第一步：执行一条命令，获取可以加载的加速器：cmd /c dir '+cwd+'\\generated\\accelerators\\').text)
            print('[配置加速器](2/3) < '+send(chat,'第二步：书写Python代码，用utf-8-sig编码读取'+cwd+'\\generated\\accelerators\\read_files.py的全部内容并输出。获取终端的输出之后，你无需再复述一遍。学习这个代码的技能。之后当我要求阅读文档时适当修改并运用你的这项技能。').text)
            print('[配置加速器](3/3) < '+send(chat,'第三步：书写Python代码阅读文件夹'+cwd+'\\generated\\accelerators\\'+'下的全部程序内容并输出。获取终端的输出之后，学习这些代码中的技能。').text)
            response = send(chat,'第四步：学习完之后你可以在我提出指定要求之后直接利用代码中的技能帮助你写新代码或执行操作。记住以上技能。完成以上操作后，加速器配置完成。请回复“代码实现加速器已加载，欢迎回来。”这句话。')
        else:
            if USE_LOCAL:
                response = send(chat, history)
            else:
                if agent_id == 0:
                    response = send(chat, PROMPT)
                elif agent_id == 1:
                    response = send(chat, MAIN_PROMPT+p_PROTECT+p_ENDING)
                elif agent_id == 2:
                    response = send(chat, BEGINNING_PROMPT+SEARCH_LOCAL_PROMPT+ENDING_PROMPT)
                elif agent_id == 3:
                    response = send(chat, BEGINNING_PROMPT+SEARCH_ONLINE_PROMPT+ENDING_PROMPT)
                elif agent_id == 4:
                    response = send(chat, BEGINNING_PROMPT+READ_FILE_PROMPT+ENDING_PROMPT)
        print('初始化完毕。')
    except ConnectionError:
            print('[ Connection Error 请确保你的网络连接稳定。 ]')
            exit()
    except requests.exceptions.ProxyError:
            print('[ Connection Unstable 请检查代理后重试。 ]')
            exit()
    except requests.exceptions.ReadTimeout:
            print('[ Connection Timeout 请检查网络连接后重试。 ]')
            exit()
    except google.api_core.exceptions.TooManyRequests:
            print('[ Too Many Requests 请求频率过高，请稍后再试。 ]')
            exit()
    except google.api_core.exceptions.InternalServerError:
            print('[ API Server Error 服务器内部错误，请重试。 ]')
            exit()
    except Exception as e:
            print('[ Python程序抛出异常：'+str(traceback.format_exc())+' ]')
            exit()
    return llm,history,chat,picmodel,tokenizer,agent_id,s2tmodel,PROMPT,response


if __name__ == "__main__":
    play_audio = True # Enable it when using interactive prompt
    llm,history,chat,picmodel,tokenizer,agent_id,s2tmodel,PROMPT,response = init()
    handle_output(response)
    turn = 1
    while True:
        print('[ 第 '+str(turn)+' 轮 ]')
        try:
            if 1:
                if agent_id == 0:
                    # 用户交互逻辑
                    if SPEECH_CONTROL:
                        in1 = input('([Enter]/键入) > ')
                        if in1 == '' or in1 == ' ':
                            msgin = transcribe(listen())
                            print('(语音) > '+msgin)
                        else:
                            msgin = in1
                    else:
                        msgin = input('(键入) > ')
                    
                    msg, use_device, building = xpost(msgin, use_device, building)
                    
                    if USE_LOCAL:
                        history.append({"role": "user", "content": msg})
                        response = send(chat,history)
                    else:
                        response = send(chat,msg)
                    
                    if building == True:
                        if DEBUG: print('< '+response)
                        print('[文档阅读完成]')
                        response = send(chat,'现在，请根据你阅读的内容，总结每个历史记录中解决用户请求的要点。对于每个历史文件，需要提取的要点包括且仅包括如下类别的内容：1、用户让编写程序的请求和你编写的最后修改版本的程序；2、用户让打开具体应用的应对策略，如对应需要执行的指令。3、对话中进行的搜索操作结果。4、用户提出一个要求，你是的最终解决方案（一句话叙述即可）。处理每个历史文件时，一律先输出文件记录时间，再给出要点。')
                        accepted = False
                        while not accepted:
                            print('(BUILDING) < '+response)
                            ask_accept = input('[ 以上总结是否需要修改？(y/n/cancel) ] > ')
                            if ask_accept == 'n':
                                accepted = True
                                with open ('acclerator.dsn','wb') as f:
                                    f.write(response.encode('utf-8'))
                                    f.close()
                                print('[ 经验加速模型构建完成 ]')
                            elif ask_accept == 'y':
                                response = send(chat,input('[ 键入修改意见 ] > '))
                            elif ask_accept == 'cancel':
                                print('[ 构建取消 ]')
                                accepted = True
            if not building:
                if USE_LOCAL:
                    for line in response:
                        if line != '':
                            chat_status = handle_output(line)
                else:
                    chat_status = handle_output(response)
            else:
                chat_status = True
                building = False
            if chat_status == False:
                break
            turn = turn + 1
            if PAUSE: input('[ 按回车键继续对话 ]')
        except KeyboardInterrupt:
            break
        except ConnectionError:
            print('[ Connection Error 请确保你的网络连接稳定。 ]')
            exit()
        except requests.exceptions.ProxyError:
            print('[ Connection Unstable 请检查代理后重试。 ]')
        except requests.exceptions.ReadTimeout:
            print('[ Connection Timeout 请检查网络连接后重试。 ]')
        except google.api_core.exceptions.TooManyRequests:
            print('[ Too Many Requests 请求频率过高，请稍后再试。 ]')
        except google.api_core.exceptions.InternalServerError:
            print('[ API Server Error 服务器内部错误，请重试。 ]')
        except Exception as e:
            print('[ Python程序抛出异常：'+str(traceback.format_exc())+' ]')

    if input('\n[ 是否保存对话历史？(y/n) ] ') == 'y':
        save_history()
    print('正在关闭内部节点...')