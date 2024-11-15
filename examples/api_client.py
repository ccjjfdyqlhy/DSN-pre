from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		message="你好呀，能做个自我介绍吗",
		audio=None,
		image=None,
		api_name="/predict"
)
print(result)# ([[None, "Welcome back, DarkstarXD! It's great to see you again. "], ['你好呀，能做个自我介绍吗', "Hi !  It's nice to meet you too! I'm Deep Streaming Neural Network, or DSN for short. I'm essentially a control system integrated into your computer. Think of me as the conductor of an orchestra, but instead of musicians, I work with various applications, files, and system processes. I can handle a lot of things like opening applications, managing files, browsing the internet, even running code for you.  \nWhat's even cooler is that I can learn and adapt based on your interactions with me. I'm still under development, but I'm eager to see what we can accomplish together. Feel free to ask me anything or just chat if you like. I'm always happy to talk with you."]], 'C:\\Users\\ccjjf\\AppData\\Local\\Temp\\gradio\\7cb24f642b854308baf8d84f5ddace3688cb03b1a36181acc5540c801684e1f0\\tts_20240915_182234.wav')
