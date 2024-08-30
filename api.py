
# DSN-API
# update 240830

from main import save_history, get_voice, send, transcribe, init
from utils import *


ver = 'Rev2_0.9.8'
BUILDNUM = 240830
cwd = os.getcwd()
platform = sys.platform
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
building = False
skip_wait = False
splits = ["，", "。", "？", "！", ",", ".", "?", "!", "~", ":", "：", "—", "…"]

chatbot_output = '初始化完毕'
filepaths = []  # 用于存储从回答中提取的文件路径


def API_get_vision_online(file_route='',prompt=''):
    if prompt == '':
            prompt = "描述分析这张图片。用中文回复。"
    if file_route == '':
            image_path = file_route
    else:
            image_path = re.sub(r'[\'\"]', '', file_route)
    try:
        image = Image.open(image_path)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content([prompt, image])
        vision_ans = response.text
    except FileNotFoundError:
        print('[ 文件不存在 ]')
    except google.api_core.exceptions.InternalServerError:
        if DEBUG: print('[ API Server Error 服务器错误 ]')
        if USE_BACKUP_VISION:
            if DEBUG: print('[ 使用本地图片识别 ]')
            raise ConnectionError
        else:
            print('[ 请开启 预加载本地视觉 配置项以在服务器出错时使用本地图片识别 ]')
    return vision_ans

def API_get_vision(file_route=''):
    if USE_ONLINE_VISION:
        try:
            return API_get_vision_online(file_route)
        except Exception as e:
            print(e)
            print('[ 使用本地图片识别 ]')
    if file_route == '':
            image_path = cwd+'\\TEMP\\latest_photo.jpg'
    else:
            image_path = file_route
    try:
        image = Image.open(image_path)
        enc_image = picmodel.encode_image(image)
        vision_ans=(picmodel.answer_question(enc_image, "Describe this image.", tokenizer))
    except FileNotFoundError:
        print('[ 文件不存在 ]')
    return vision_ans

def handle_output(output, chat_history, execute_layer=1):
    global filepaths  # 访问全局变量 filepaths
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
        result = '[控制系统输出]用户正在使用远程API，无法使用视觉。请你引导用户通过上传图片让分析以使用视觉。'
        skipreturn = False
    elif output.startswith('[IMG]'):
        process = output.split(' ')
        print('[ 分析图片：'+process[1]+' ]')
        try:
            result = API_get_vision(file_route=process[1],prompt=process[2])
        except IndexError:
            result = API_get_vision(file_route=process[1])
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
            ttsfiles = []
            beautifiedoutput, filepaths = beautify(output)
            if DEBUG: print(filepaths)
            current_line = 1
            for line in [x for x in beautifiedoutput.split('\n') if x]:
                print('[ 段落 '+str(current_line)+' ]')
                if line != '' and line != '\n':
                    if line.endswith('。'):
                        linelength = len(line.split('。'))-1
                    else:
                        linelength = len(line.split('。'))
                    if DEBUG: print(line.split('。'))
                    else: 
                        print('[ 构建回答... 总数：'+str(linelength)+' ]')
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
                                            ttsfiles.append("TEMP\latest_generated.wav")
                                        elif TTS_MODEL_NAME == 'Venti-CN':
                                            get_voice(
                                                refer_wav=TTS_MODEL_PATH+r"/audios/emotion_templates/#calm2.wav",#TODO
                                                refer_text="蒲公英子就像自然的宝石，汇聚着每年第一缕风。人们把它放进酒桶，就是把当下的风放了进去。",
                                                prompt_language='zh',
                                                text=sentence,
                                            )
                                            ttsfiles.append("TEMP\latest_generated.wav")
                                        elif TTS_MODEL_NAME == '温迪':
                                            get_voice(
                                                refer_wav=TTS_MODEL_PATH+r"/audios/emotion_templates/#calm2.wav",#TODO
                                                refer_text="蒲公英子就像自然的宝石，汇聚着每年第一缕风。人们把它放进酒桶，就是把当下的风放了进去。",
                                                prompt_language='zh',
                                                text=sentence,
                                            )
                                            ttsfiles.append("TEMP\latest_generated.wav")
                                    elif LANG == 'English':
                                        get_voice(
                                            refer_wav=TTS_MODEL_PATH+r"/audios/Venti/test.wav",#TODO
                                            refer_text="Many people may feel lost at times. After all, it's impossible for everything to happen according to your own wishes.",
                                            prompt_language='en',
                                            text=sentence,
                                        )
                                        ttsfiles.append("TEMP\latest_generated.wav")
                                    else:
                                        print('[ TTS Language not supported. ]')
                                        chat_history[-1][1] += "[ TTS Language not supported. ]\n"
                                        yield chat_history, None
                                    print(' ['+str(current_sentence)+'/'+str(linelength)+'] '+sentence)
                                    chat_history[-1][1] += f"{sentence}\n"
                                    for item in ttsfiles:
                                        if DEBUG: print('< '+item)
                                        yield chat_history, item  # 将当前语音文件路径传递给Gradio
                                        ttsfiles = []  # 清空已播放的语音文件路径
                                    current_sentence += 1
                current_line += 1
        else:
            print('< '+output)
            chat_history[-1][1] += f"{output}\n"
            yield chat_history, None
        result=''
        skipreturn = True
    if not skipreturn:
        if str(result) == '' or result == '[]':
            response = send(chat,'[控制系统返回] 操作成功完成。')
            print('[ 第 '+str(execute_layer)+' 层动作完成 ]')
            chat_history[-1][1] += response + "\n"
            yield chat_history, None
        else:
            if execute_layer >= 10 and execute_layer <= LAYERS_LIMIT:
                print('[ 第 '+str(execute_layer)+' 层动作完成 / 自纠错限制: '+LAYERS_LIMIT+'层 ]')
                execute_layer = execute_layer + 1
                response = send(chat,'[控制系统返回] '+str(result))
                yield from handle_output(response, chat_history, execute_layer)  # 递归调用并传递chat_history
            elif execute_layer > LAYERS_LIMIT:
                print('[ 第 '+str(execute_layer)+' 层动作完成 / 达到最大纠错层数 ]')
                response = send(chat,'停止尝试纠正，错误次数太多。请详细描述遇到的错误，以便我们一起解决它。')
                print('< '+response)
                chat_history[-1][1] += response + "\n"
                yield chat_history, None
            else:
                print('[ 第 '+str(execute_layer)+' 层动作完成 ]')
                execute_layer = execute_layer + 1
                response = send(chat,'[控制系统返回] '+str(result))
                yield from handle_output(response, chat_history, execute_layer) # 递归调用并传递chat_history

def APIpost(msgin, building):
    if msgin == 'BUILD_TRAIN_DATA' or msgin == '构建加速模型':
        building = True
        return '请你阅读'+cwd+'\\generated\\chat_history\\文件夹下的全部内容。'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = "系统UTC+8时间："+timestamp+" 用户输入："+msgin
    return msg, building

def predict(message, chat_history, audio=None, image=None):
    """处理消息、音频、图像并更新聊天历史"""
    global chatbot_output, building, vision_result, result
    vision_result = ''
    if message != '':
        chat_history.append([message, ''])
        if audio is not None and image is None:
            chat_history.append(['[ 音频 ]', ''])
        elif image is not None and audio is None:
            chat_history.append(['[ 图片 ]', ''])
        elif audio is not None and image is not None:
            chat_history.append(['[ 音频和图片 ]', ''])
    else:
        if audio is not None and image is None:
            chat_history.append(['[ 音频 ]', ''])
        elif image is not None and audio is None:
            chat_history.append(['[ 图片 ]', ''])
        elif audio is not None and image is not None:
            chat_history.append(['[ 音频和图片 ]', ''])
        else:
            return
    yield chat_history, None
    try:
        if audio is not None:
            audio_path = audio
            message = transcribe(audio_path)
            print(f"(语音) > {message}")
        if image is not None:
            image_path = image
            message = f"{VISION_START2} {vision_result} 用户输入：{message}，附件：{image_path}"

        msg, building = APIpost(msgin=message, building=building)

        if USE_LOCAL:
            history.append({"role": "user", "content": msg})
            response = send(msgcontent=history)
        else:
            response = send(chat, msg)
        yield from handle_output(response, chat_history)  
    except (ConnectionError, requests.exceptions.ProxyError, 
            requests.exceptions.ReadTimeout, google.api_core.exceptions.TooManyRequests, 
            google.api_core.exceptions.InternalServerError) as e:
        chat_history[-1][1] += f"[ API网络错误，请重新发送 ]\n"
        yield chat_history, None
    except Exception as e:
        chat_history[-1][1] += f"[ Python程序抛出异常：{str(traceback.format_exc())} ]\n"
        yield chat_history, None

def init_chatbot():
    """初始化聊天机器人，加载模型等"""
    global llm, history, chat, picmodel, tokenizer, agent_id, s2tmodel, PROMPT, chatbot_output, response
    llm, history, chat, picmodel, tokenizer, agent_id, s2tmodel, PROMPT, response = init(
        silent=True
    )
    chatbot_output = response
    return chatbot_output

def main():
    """创建 Gradio 界面"""
    global chatbot_output,chat_history
    chatbot_output = init_chatbot()
    with gr.Blocks(title="DSN-API", theme=gr.themes.Soft()) as app:
        with gr.Row():
            with gr.Column():
                chatbot = gr.Chatbot([[None, chatbot_output]],label="互动 / Interaction")
                tts_audio = gr.Audio(label="响应 / Response", autoplay=True)
            with gr.Column():
                msg = gr.Textbox(placeholder="输入内容... / Type something...", label="提示 / Prompt")
                with gr.Row():
                    audio = gr.Audio(type="filepath", label="上传音频 / Upload audio")
                    image = gr.Image(type="filepath", label="上传图像 / Upload image")
                with gr.Row(): 
                    submit = gr.Button("发送 / Send")

        submit.click(
            predict, inputs=[msg, chatbot, audio, image], outputs=[chatbot, tts_audio]
        )
        msg.submit(
            predict, inputs=[msg, chatbot, audio, image], outputs=[chatbot, tts_audio]
        )

    app.launch()
    app.close(save_history(api_tag=True))

if __name__ == "__main__":
    main()