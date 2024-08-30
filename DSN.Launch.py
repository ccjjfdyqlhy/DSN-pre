from config import PYTHON
import os

cwd = os.getcwd()

os.system('cmd /c start '+PYTHON+' '+cwd+'\\main.py')