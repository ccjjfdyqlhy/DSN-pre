import os
import sys
import datetime

cwd = os.getcwd()
folder = os.path.join(cwd, "TEMP")
cmd_file = os.path.join(folder, "latest_cmd.txt")

# 从 latest_cmd.txt 文件中读取命令
try:
    with open(cmd_file, "r", encoding="utf-8-sig") as f:
        output = f.readline().strip()  # 读取第一行并去除空格
except FileNotFoundError:
    print("错误：找不到 latest_cmd.txt 文件")
    sys.exit(1)  # 退出程序，返回错误代码

# 检测并去除 "cmd /c" 前缀
if output.startswith("cmd /c"):
    output = output[len("cmd /c"):].strip()

# 检测并添加 "start" 前缀 (Windows only)
if not output.startswith("start"):
    output = "start " + output

result = str(os.popen(output + ' 2>&1').readlines())

if not os.path.exists(folder):
    os.makedirs(folder)
with open(os.path.join(folder, "cmd_output.txt"), "w", encoding="utf-8-sig") as f:
    f.write(result) 