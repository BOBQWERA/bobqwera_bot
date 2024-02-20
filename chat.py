import json
import os
from utils import Ok, Error, Result, askChatGPT, error_handle


class BotStatus:
    def __init__(self):
        self.status = 'waiting'
        self.use_audio = False

    def set_status(self, status):
        self.status = status

    def to_string(self):
        return self.status
    
    @staticmethod
    def from_string(status):
        bot_status = BotStatus()
        bot_status.set_status(status)
        return bot_status

    def __getattr__(self, name):
        if name.startswith('is_'):
            return self.status == name[3:]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class ChatGPT:
    def __init__(self, messages,user,system_mode='normal'):
        self.messages = messages
        self.user = user
        self.system = None
        self.system_mode = system_mode
        self.bot_status = BotStatus()
        
    def set_system(self, system: str):
        self.system = {
            "role": "system",
            "content": system
        }

    def set_system_mode(self, system_mode: str):
        self.system_mode = system_mode

    def clear(self):
        self.messages = []
        self.system = None

    def to_json(self,path):
        with open(path, 'w') as f:
            f.write(json.dumps(
                {
                    "messages": self.messages,
                    "system": self.system,
                    "system_mode": self.system_mode,
                    "status": self.bot_status.to_string()
                }
            ))
    
    @staticmethod
    def from_json(path):
        with open(path, 'r') as f:
            data = json.load(f)
            chatgpt = ChatGPT(data['messages'],data['system_mode'])
            chatgpt.system = data['system']
            chatgpt.bot_status = BotStatus.from_string(data['status'])
            return chatgpt
        
    def save(self,name):
        if os.path.exists(f"data/{self.user}/{name}.json"):
            return Error("文件已存在")
        self.to_json(f"data/{self.user}/{name}.json")
        return Ok("保存成功")

    def load(self,index):
        if not os.path.exists(f"data/{self.user}/{index}.json"):
            return Error("文件不存在")
        return ChatGPT.from_json(f"data/{self.user}/{index}.json")

    @error_handle
    def ask(self, text) -> Result:
        if self.system is None:
            return Error("还没有设置人设")
        d = {"role": "user", "content": text}
        self.messages.append(d)
        print("问了ChatGPT")
        text = askChatGPT([self.system,]+self.messages)
        if not text:
            self.messages.pop()
            return Error("ChatGPT出错了")
        else:
            d = {"role": "assistant", "content": text}
            self.messages.append(d)
            return Ok(text)

