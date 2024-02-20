import requests


def get_token():
    with open("TOKEN", "r") as file:
        return file.read().strip()
    

def askChatGPT(messages):
    url = "https://openkey.cloud/v1/chat/completions"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-iFZCqiwRbz48hpRbbSpOZT7HY8nlviK50Cbd6yosfiO6A2GA'
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)
    res_json = response.json()

    try:
        text = res_json['choices'][0]['message']['content']
        return text
    except:
        return "[Error]："+str(res_json)
    

def error_handle(func):
    def wrapper(self, *args, **kwargs)->Result:
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            return Error('以下是错误信息：\n' + str(e) + '\n请联系管理员')
    return wrapper
    

class Result:
    def __init__(self, text, status:bool):
        self.text = text
        self.status = status

    def parse(self):
        return self.text, self.status

class Ok(Result):
    def __init__(self, text):
        super().__init__(text, True)

class Error(Result):
    def __init__(self, text):
        super().__init__(text, False)
    

if __name__ == "__main__":
    print(get_token())