from gradio_client import Client, handle_file
import subprocess, re, os, datetime

PYTHON = "python"
cwd = os.getcwd()
client = Client("http://127.0.0.1:7860/")

def extract_code(output):
    """提取代码块中的代码"""
    match = re.search(r"```python(.*?)```", output, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def run_command_or_code(output):
    """运行命令或代码并返回输出"""
    iostream = ""
    if output.startswith('cmd /c'):
        folder = cwd + "\\TEMP\\"
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(folder + 'latest_cmd.txt', "w", encoding="utf-8-sig") as f:
            f.write(output)
        subprocess.Popen([PYTHON, cwd + '\\cmdctrl.py'])  # 假设 cmdctrl.py 用于执行命令并输出到 cmd_output.txt
        with open(folder + 'cmd_output.txt', "r", encoding="utf-8-sig") as f:
            iostream = f.read()
    elif output.startswith('```python'):
        folder = cwd + "\\generated\\program_history"
        if not os.path.exists(folder):
            os.makedirs(folder)
        time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        history_file_path = os.path.join(folder, f"program{time_str}.py")
        code_content = extract_code(output)
        with open(history_file_path, "w", encoding="utf-8-sig") as f:
            f.write(code_content)
        if not os.path.exists('TEMP'):
            os.makedirs('TEMP')
        with open(cwd + '\\TEMP\\historydest.txt', 'w', encoding='utf-8') as f:
            f.write(history_file_path)
        coderunner = subprocess.Popen([PYTHON, cwd + '\\coderunner.py'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # 假设 coderunner.py 用于执行Python代码并输出结果
        stdout, stderr = coderunner.communicate()
        iostream = stdout.decode('gbk') + stderr.decode('gbk')
    if iostream == '' or iostream == '[]':
        iostream = '无输出，操作可能成功完成。'
    return iostream

def is_code_response(output):
    """判断回复是否包含代码"""
    return output.startswith('cmd /c') or output.startswith('```python')

def get_user_input():
    """获取用户输入的文本或模态信息"""
    message = input("请输入文本信息（或按回车跳过）：")
    audio_file = None
    image_file = None
    if message == "":
        audio_file = input("请输入音频文件路径（或按回车跳过）：")
        if audio_file == "":
            image_file = input("请输入图片文件路径（或按回车跳过）：")
    return message, audio_file, image_file

# 初始化聊天历史
chat_history = []

while True:
    # 获取用户输入
    message, audio_file, image_file = get_user_input()

    # 发送用户输入到服务端
    result = client.predict(
        message=message,
        audio=handle_file(audio_file) if audio_file else None,
        image=handle_file(image_file) if image_file else None,
        iostream="",
        api_name="/predict"
    )

    # 处理服务端返回的结果
    chat_history, _, _ = result 
    last_output = chat_history[-1][1]

    # 判断回复是否包含代码
    if is_code_response(last_output):
        # 运行代码并获取输出
        iostream = run_command_or_code(last_output)
        if iostream:
            # 将代码执行结果发送到服务端
            result = client.predict(
                message="",
                audio=None,
                image=None,
                iostream=iostream,
                api_name="/predict"
            )
            chat_history, _, _ = result
    else:
        # 打印AI的回复
        print(f"AI: {last_output}")

    # 打印当前聊天历史
    print("--------------------")
    for user_msg, ai_msg in chat_history:
        if user_msg:
            print(f"用户: {user_msg}")
        if ai_msg:
            print(f"AI: {ai_msg}")
    print("--------------------")