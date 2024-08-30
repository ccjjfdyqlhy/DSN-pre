import random
import os,sys
from subprocess import Popen
from config import python_exec

def get_audio_file(text):
  """
  根据输入的字符串中包含的词汇(active、calm、question、poor、derivation、enjoyment、poetic)来决定选择的音频文件，并从一个文件夹下随机选择文件名带有相应词汇的.wav声音文件，返回该文件的绝对路径。

  Args:
    text (str): 输入的字符串。

  Returns:
    str: 声音文件的绝对路径。
  """

  # 根据输入的字符串中包含的词汇决定语调
  tones = ["active", "calm", "question", "poor", "derivation", "enjoyment", "poetic"]
  for tone in tones:
    if tone in text:
      break

  # 从文件夹中随机选择一个带有相应语气的.wav声音文件
  folder_path = os.path.join(os.path.dirname(__file__), "sounds")
  files = [f for f in os.listdir(folder_path) if f.endswith(".wav") and tone in f]
  file = random.choice(files)

  # 返回声音文件的绝对路径
  return os.path.join(folder_path, file)
