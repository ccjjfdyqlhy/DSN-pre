from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		message="你好呀，能做个自我介绍吗",
		chat_history=[[None,"欢迎回来。"]],
		audio=None,
		image=None,
		api_name="/predict"
)
print(result)