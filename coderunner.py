import os
from config import PYTHON
cwd = os.getcwd()
f=open(cwd+'\\TEMP\\historydest.txt','r',encoding='utf-8')
coderunner = os.popen(PYTHON+' '+f.read()+' 2>&1')
result = str(coderunner.readlines())
print(result)