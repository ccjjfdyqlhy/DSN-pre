
# DSN utility functions
# update 240830

from prompt import *
try:
    from config import *
except:
    print("请先使用congif-ui.py设定配置，生成config.py，再启动程序。")
    exit()

import google.generativeai as genai
import numpy as np
import gradio as gr
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from funasr import AutoModel
from llama_cpp import Llama
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import os,sys,requests,win32gui,win32api,psutil,cv2,pyaudio,google.api_core,time,wave,traceback,datetime,subprocess,re

splits = ["，", "。", "？", "！", ",", ".", "?", "!", "~", ":", "：", "—", "…"]

def chattts(required_text):
    res = requests.post('http://127.0.0.1:9966/tts', data={
  "text": required_text,
  "prompt": "",
  "voice": "2222",
  "temperature": CHATTTS_TEMP,
  "top_p": 0.7,
  "top_k": 20,
  "refine_max_new_token": "384",
  "infer_max_new_token": "2048",
  "skip_refine": 0,
  "is_split": 1,
  "custom_voice": CHATTTS_SEED
})
    return res

def get_cursored_hwnd():
    cursor_point = win32api.GetCursorPos()  
    hwnd = win32gui.WindowFromPoint(cursor_point)
    return hwnd

def get_dailyinfo():
    rep = requests.get('http://v1.yiketianqi.com/api?unescape=1&version=v91&appid=99245552&appsecret=RL8NtmPx&ext=&city='+CITY)
    rep.encoding = 'utf-8'
    return rep.json()

def check_process(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False

def start_everything():
    # 启动 Everything.exe
    try:
        subprocess.Popen(cwd+'\\binaries\\Everything.exe', shell=True)
    except FileNotFoundError:
        print('未安装 Everything，请前往安装')
        exit()

def start_chattts():
    # 启动 Chatts.exe
    try:
        subprocess.Popen('cmd /c start '+cwd+'\\instances\\chattts\\app.exe', shell=True)
    except FileNotFoundError:
        print('未安装 ChatTTS，请前往安装')
        exit()

def start_tts():
    try:
        subprocess.Popen('cmd /c start '+TTS_PYTHON+' '+cwd+'\\instances\\DSN-vocal\\GPT_SoVITS\\DSN-Vocal-api.py -d "cuda" -s '+TTS_MODEL_PATH+'\\SoVITS_weights\\'+TTS_MODEL_NAME+'.pth -g '+TTS_MODEL_PATH+'\\GPT_weights\\'+TTS_MODEL_NAME+'.ckpt', shell=True)
    except FileNotFoundError:
        print('未安装 DSN-vocal，请前往安装')
        exit()

def remove_extension(filename):
    if '.' in filename:
        return filename.split('.')[0]
    else:
        return filename

def search_file_by_name(file_name):
    search_result = str(os.popen(cwd+'\\binaries\\search_everything.exe wfn:'+file_name+' 2>&1').readlines())
    if len(search_result) > 0:
        return search_result
    else:
        return 'No result found'

def search_file_by_kind(file_kind, keyword):
    search_result = []
    file_kinds = ['audio','zip','doc','exe','pic','video']
    audio = ['mp3','wav','aac','flac','wma','ogg']
    zipname = ['zip','rar','7z','iso']
    doc = ['doc','docx','ppt','pptx','xls','xlsx','pdf']
    exe = ['exe','msi','bat','cmd']
    pic = ['jpg','jpeg','png','gif','bmp','tiff']
    video = ['mp4','avi','mov','wmv','flv','mkv']
    i = 0
    keyword = remove_extension(keyword)
    if file_kind == 'audio':
        for name in audio:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'zip':
        for name in zipname:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'doc':
        for name in doc:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'exe':
        for name in exe:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'pic':
        for name in pic:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'video':
        for name in video:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    else:
        return 'Invalid file kind, please choose one: '+str(file_kinds)
    if len(search_result) > 0:
        return str(search_result)
    else:
        return 'No result found'
    
def search_file_by_keyword(keyword):
    search_result = str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+' 2>&1').readlines())
    if len(search_result) > 0:
        return search_result
    else:
        return 'No result found'

def get_vision_online(use_file=False,file_route='',prompt=''):
    if use_file:
        if prompt == '':
            prompt = "描述分析这张图片。用中文回复。"
        if file_route == '':
            image_path = input('[ 键入图片路径 ] > ')
            print('使用本地图片：'+image_path)
        else:
            image_path = re.sub(r'[\'\"]', '', file_route)
    else:
        prompt = '用中文回复你看到了什么。'
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

def extract_code(md_string):
    code_box = re.search(r'```python(.*?)```', md_string, re.DOTALL)
    if code_box:
        code = code_box.group(1)
        return code.strip()
    else:
        return None

def extract_model_output(response_json):
    match = re.search(r"'content': '(.*?)'", response_json)
    if match:
        return match.group(1).split(r'\n')
    else:
        return []

def beautify(text):
    placeholder = "这个位置"
    filepath_pattern = r"(?:\"(?:[a-zA-Z]:)?(?:/[\w\s\.\-]+)+\"|'(?:[a-zA-Z]:)?(?:/[\w\s\.\-]+)+'|(?:[a-zA-Z]:)?(?:/[\w\s\.\-]+)+|(?:[A-Za-z]:\\[\w\s\.\-\\]+)+)"
    filepaths = re.findall(filepath_pattern, text)
    replaced_text = re.sub(filepath_pattern, placeholder, text)
    replaced_text = replaced_text.replace(USERNAME + '的', "你的")
    replaced_text = replaced_text.replace(USERNAME + '，', "")
    replaced_text = replaced_text.replace(USERNAME, "")
    for i in range(len(splits)):
        replaced_text = replaced_text.replace(AI_NAME + splits[i], "")
    replaced_text = replaced_text.replace(AI_NAME, "")
    replaced_text = replaced_text.replace("**", "")
    code_block_pattern = r"```.*?```"
    replaced_text = re.sub(code_block_pattern, "", replaced_text, flags=re.DOTALL)
    return replaced_text, filepaths

def listen():
    temp = 20
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    mindb=2000
    delayTime=1.3
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    #snowboydecoder.play_audio_file()
    print("[ 请说出指令 ]")
    frames = []
    flag = False
    stat = True
    stat2 = False
    tempnum = 0
    tempnum2 = 0
    while stat:
        data = stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        if temp > mindb and flag==False:
            flag =True
            print("[ 监听指令中 ]")
            tempnum2=tempnum
        if flag:
            if(temp < mindb and stat2==False):
                stat2 = True
                tempnum2 = tempnum
                if DEBUG: print("关键点记录")
            if(temp > mindb):
                stat2 =False
                tempnum2 = tempnum
            if(tempnum > tempnum2 + delayTime*15 and stat2==True):
                if DEBUG: print("%.2lfs后开始检查关键点"%delayTime)
                if(stat2 and temp < mindb):
                    stat = False
                else:
                    stat2 = False
        #print(str(temp)  +  "      " +  str(tempnum))
        tempnum = tempnum + 1
        if tempnum > EXCEED_TIME:
            stat = False
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(cwd+'\\TEMP\\latest_record.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return cwd+'\\TEMP\\latest_record.wav'