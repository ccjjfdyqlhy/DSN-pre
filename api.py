
# DSN-API
# update 241115

from main import save_history, get_voice, send, transcribe, init
from utils import *

try:
    if sys.argv[1] == 'backend':
        SHORT_ANS = True
except:
    SHORT_ANS = False

ver = 'Rev2_IOmod_2.2.0'
BUILDNUM = 241115
platform = sys.platform
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
export_prompt = False  # Set to True to export prompts to prompt.txt
building = False
skip_wait = False
splits = ["，", "。", "？", "！", ",", ".", "?", "!", "~", ":", "：", "—", "…"]

chatbot_output = '初始化完毕'
filepaths = []  # 用于存储从回答中提取的文件路径

def API_get_vision_online(file_route='', prompt=''):
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

def API_get_vision(file_route='', prompt=''):
    if USE_ONLINE_VISION:
        try:
            return API_get_vision_online(file_route, prompt)
        except Exception as e:
            print(e)
            print('[ 使用本地图片识别 ]')
    if file_route == '':
        image_path = cwd + '\\TEMP\\latest_photo.jpg'
    else:
        image_path = file_route
    try:
        image = Image.open(image_path)
        enc_image = picmodel.encode_image(image)
        vision_ans = picmodel.answer_question(enc_image, "Describe this image.", tokenizer)
    except FileNotFoundError:
        print('[ 文件不存在 ]')
    return vision_ans

def handle_output(output, chat_history, execute_layer=1, audio_files=[], silent=False, iostream=""):
    global filepaths
    if output.startswith('cmd /c') or output.startswith('```python'):
        iscode = True
    elif output.startswith('```tool_code'):
        iscode = True
    else:
        iscode = False
    if '[SAVE_MEMO]' in output:  # Server-side save memo to long-term memory
        content = output.split('[SAVE_MEMO] ', 1)[1]
        with open(cwd + "\\generated\\longterm_memory.txt", "a", encoding="utf-8-sig") as f:
            f.write(remove_extra_newlines(content) + "\n")
            f.close()
        print('[记录了内容] '+remove_extra_newlines(content))
        output = output.split('[SAVE_MEMO]')[0]
    if '[GETDAILYINFO]' in output: # Server-side
        result = str(get_dailyinfo())
        if DEBUG: print('[ 获取今日信息 ]')
        skipreturn = False
    elif output == '[VISION]': # Does not work
        result = '[控制系统输出]用户正在使用远程API，无法使用视觉。请你引导用户通过上传图片让分析以使用视觉。'
        skipreturn = False
    elif output.startswith('[IMG]'): # um...
        process = output.split(' ')
        print('[ 分析图片：' + process[1] + ' ]')
        try:
            result = API_get_vision(file_route=process[1], prompt=process[2])
        except IndexError:
            result = API_get_vision(file_route=process[1])
        skipreturn = False
    elif '[SAVE_HISTORY]' in output: # Should be server-side
        save_history()
        print('[ 聊天记录已存档 ]')
        result = ''
        skipreturn = False
    elif output.startswith('[END_CONVERSATION]'): # will not work
        print('[' + AI_NAME + ' 结束了对话。]')
        print("重新启动程序以继续。")
        return False
    else: # Is normal message; handle TTS
        if TEXT_TO_SPEECH and not silent and not iscode:
            ttsfiles = []
            output = beautify_display(output)
            beautifiedoutput, filepaths = beautify(output)
            if DEBUG: print(filepaths)
            current_line = 1
            current_sentence = 1
            # Split both output and beautifiedoutput into sentences using the same logic
            sentences_output = []
            sentences_beautified = []
            for line in [x for x in output.split('\n') if x]:
                if line.endswith('。'):
                    sentences_output.extend(line.split('。')[:-1])
                else:
                    sentences_output.extend(line.split('。'))
            for line in [x for x in beautifiedoutput.split('\n') if x]:
                if not line.endswith('。'):
                    line += '。'  # 在末尾添加句号
                sentences_beautified.extend(line.split('。')[:-1])

            # Ensure both lists have the same number of sentences
            if len(sentences_output) != len(sentences_beautified):
                print("LOGICAL ERROR: Sentence splitting mismatch!")
                print(sentences_output)
                print(sentences_beautified)
            # assert len(sentences_output) == len(sentences_beautified), "Sentence splitting mismatch!"
            if DEBUG:
                print(sentences_output)
                print(sentences_beautified)
            for sentence_output, sentence_beautified in zip(sentences_output, sentences_beautified):
                if sentence_beautified != '' and sentence_beautified != '\n' and sentence_beautified != ' ':
                    print('[ 段落 ' + str(current_line) + ' ]')
                    # Synthesize audio using beautified sentence
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    audio_folder = cwd + "\\generated\\tts_history"
                    if not os.path.exists(audio_folder):
                        os.makedirs(audio_folder)
                    audio_file = os.path.join(audio_folder, f"tts_{timestamp}.wav")
                    if USE_CHATTTS:
                        chattts(sentence_beautified)
                    else:
                        # Read references from file
                        references = {}
                        with open(TTS_MODEL_PATH + "/references.txt", "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith("#"):
                                    model_name, refer_wav, refer_text, prompt_language = line.split("|")
                                    references[model_name] = {
                                        "refer_wav": TTS_MODEL_PATH + "/" + refer_wav,
                                        "refer_text": refer_text,
                                        "prompt_language": prompt_language,
                                    }
                        if TTS_MODEL_NAME in references:
                            ref = references[TTS_MODEL_NAME]
                            get_voice(
                                refer_wav=ref["refer_wav"],
                                refer_text=ref["refer_text"],
                                prompt_language=ref["prompt_language"],
                                text=sentence_beautified,
                                filename=audio_file
                            )
                        elif LANG == 'English':
                            # Fallback to English if model not found in references and language is English
                            get_voice(
                                refer_wav=TTS_MODEL_PATH + r"/audios/Venti/test.wav",
                                refer_text="Many people may feel lost at times. After all, it's impossible for everything to happen according to your own wishes.",
                                prompt_language='en',
                                text=sentence_beautified,
                                filename=audio_file
                            )
                        else:
                            print('[ TTS Model or Language not supported. ]')
                            chat_history[-1][1] += "[ TTS Model or Language not supported. ]\n"
                            yield chat_history, None, audio_files
                        ttsfiles.append(audio_file)
                    print(' [' + str(current_sentence) + '/' + str(len(sentences_beautified)) + '] ' + sentence_beautified)
                    # Add original sentence to chat history
                    chat_history[-1][1] += f"{sentence_output}。\n"
                    for item in ttsfiles:
                        if DEBUG: print('< ' + item)
                        audio_files.append(item)  # 添加音频文件到列表
                        yield chat_history, item, audio_files  # yield 聊天历史、当前音频文件和音频文件列表
                        ttsfiles = []
                    current_sentence += 1
                if sentence_output.endswith('。'):
                    current_line += 1
        else:
            print('< ' + output)
            chat_history[-1][1] += f"{output}\n"
            yield chat_history, None, audio_files  # yield 聊天历史、None和音频文件列表
        result = ''
        skipreturn = True
    if not skipreturn:
        if str(result) == '' or result == '[]' or iostream != "":  # 新增对iostream 的判断
            if iostream != "":
                response = send(chat, '[控制系统返回] ' + iostream) # 使用iostream作为回复
            else:
                response = send(chat, '[控制系统返回] 操作成功完成。')
            print('[ 第 ' + str(execute_layer) + ' 层动作完成 ]')
            chat_history[-1][1] += response + "\n"
            yield chat_history, None, audio_files  # yield 聊天历史、None和音频文件列表
        else:
            if execute_layer >= 10 and execute_layer <= LAYERS_LIMIT:
                print('[ 第 ' + str(execute_layer) + ' 层动作完成 / 自纠错限制: ' + LAYERS_LIMIT + '层 ]')
                execute_layer = execute_layer + 1
                response = send(chat, '[控制系统返回] ' + str(result))
                yield from handle_output(response, chat_history, execute_layer, audio_files, iostream="")  # 传递 audio_files
            elif execute_layer > LAYERS_LIMIT:
                print('[ 第 ' + str(execute_layer) + ' 层动作完成 / 达到最大纠错层数 ]')
                response = send(chat, '停止尝试纠正，错误次数太多。请详细描述遇到的错误，以便我们一起解决它。')
                print('< ' + response)
                chat_history[-1][1] += response + "\n"
                yield chat_history, None, audio_files  # yield 聊天历史、None和音频文件列表
            else:
                print('[ 第 ' + str(execute_layer) + ' 层动作完成 ]')
                execute_layer = execute_layer + 1
                response = send(chat, '[控制系统返回] ' + str(result))
                yield from handle_output(response, chat_history, execute_layer, audio_files, iostream="")  # 传递 audio_files

def APIpost(msgin, building, silent):
    if msgin == 'BUILD_TRAIN_DATA' or msgin == '构建加速模型':
        building = True
        return '请你阅读' + cwd + '\\generated\\chat_history\\文件夹下的全部内容。'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = "系统UTC+8时间：" + timestamp + " 用户输入：" + msgin
    return msg, building

def predict(message, chat_history, audio=None, image=None, silent=False, iostream=""):
    """处理消息、音频、图像、iostream 并更新聊天历史"""
    global chatbot_output, building, vision_result, result
    vision_result = ''

    # 处理不同类型的输入
    if message != "":
        chat_history.append([message, ''])
    if audio is not None:
        chat_history.append(['[ 音频 ]', ''])
    if image is not None:
        chat_history.append(['[ 图片 ]', ''])
    if iostream != "":
        chat_history.append(['[ iostream ]', ''])

    # 如果没有任何输入，则直接返回
    if message == "" and audio is None and image is None and iostream == "":
        return

    yield chat_history, None, []  # yield 聊天历史、None和空音频文件列表

    try:
        if audio is not None:
            audio_path = audio
            message = '(你听到的语音消息)'+transcribe(audio_path)
            print(f"(语音) > {message}")
        if image is not None:
            image_path = image
            message = f"{VISION_START2} {vision_result} 用户输入：{message}，附件：{image_path}"
        if iostream != "":  # 处理 iostream 输入
            message = f"[控制系统返回] {iostream}"

        msg, building = APIpost(msgin=message, building=building, silent=silent)

        if USE_LOCAL:
            history.append({"role": "user", "content": msg})
            response = send(msgcontent=history)
        else:
            response = send(chat, msg)
        
        # 在开始处理新的回复之前清空 audio_files 列表
        yield from handle_output(response, chat_history, 1, [], silent=silent, iostream="") 
    
    except (ConnectionError, requests.exceptions.ProxyError,
            requests.exceptions.ReadTimeout, google.api_core.exceptions.TooManyRequests,
            google.api_core.exceptions.InternalServerError) as e:
        chat_history[-1][1] += f"[ API网络错误，请重新发送 ]\n"
        yield chat_history, None, []  # yield 聊天历史、None和空音频文件列表
    except Exception as e:
        chat_history[-1][1] += f"[ Python程序抛出异常：{str(traceback.format_exc())} ]\n"
        yield chat_history, None, []  # yield 聊天历史、None和空音频文件列表


def init_chatbot():
    """初始化聊天机器人，加载模型等"""
    global llm, history, chat, picmodel, tokenizer, agent_id, s2tmodel, PROMPT, chatbot_output, response
    llm, history, chat, picmodel, tokenizer, agent_id, s2tmodel, PROMPT, response = init(
        silent=True,
        short=SHORT_ANS,
        export=export_prompt,
    )
    chatbot_output = response
    return chatbot_output

def reset_user_input():
    return gr.update(value='')

def main():
    """创建 Gradio 界面"""
    global chatbot_output, chat_history
    chatbot_output = init_chatbot()
    with gr.Blocks(title="DSN-API", theme='soft') as app:
        gr.Markdown("本webUI仅供调试使用，可能会有很多潜在的BUG。要用于生产环境，请使用[DodoUI](https://github.com/ccjjfdyqlhy/DodoUI)。")
        with gr.Row():
            with gr.Column():
                chatbot = gr.Chatbot([[None, chatbot_output]], label="互动 / Interaction")
                with gr.Row():
                    tts_audio = gr.Audio(label="响应 / Response", autoplay=True)
                    audio_files = gr.Files(label="音频文件 / Audio Files", visible=True)
            with gr.Column():
                msg = gr.Textbox(placeholder="输入内容... / Type something...", label="提示 / Prompt")
                with gr.Row():
                    audio = gr.Audio(type="filepath", label="上传音频 / Upload audio")
                    image = gr.Image(type="filepath", label="上传图像 / Upload image")
                with gr.Row():
                    silent_checkbox = gr.Checkbox(label="静音")
                    iostream = gr.Textbox(label="iostream")  #  iostream输入框
                    submit = gr.Button("发送 / Send")

        submit.click(
            predict, inputs=[msg, chatbot, audio, image, silent_checkbox, iostream], outputs=[chatbot, tts_audio, audio_files]
        )
        submit.click(lambda: reset_user_input(), outputs=msg)
        msg.submit(
            predict, inputs=[msg, chatbot, audio, image, silent_checkbox, iostream], outputs=[chatbot, tts_audio, audio_files]
        )
        msg.submit(lambda: reset_user_input(), outputs=msg)

    app.launch(server_name='0.0.0.0', server_port=7860)
    app.close(save_history(api_tag=True))

if __name__ == "__main__":
    main()