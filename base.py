# base.py (пример добавления)
import os
import openai  # или direct HTTP-запросы

class AIAgent:
    def __init__(self, system_prompt: str, deepseek_api_key: str):
        self.system_prompt = system_prompt
        self.api_key = deepseek_api_key
        self.memories: Dict[str, list] = {}

    def process_message(self, user_id: str, message: str) -> str:
        # Добавляем сообщение в историю
        if user_id not in self.memories:
            self.memories[user_id] = []
        self.memories[user_id].append({"role": "user", "content": message})

        # Формируем payload для DeepSeek API
        # (здесь можно использовать openai-совместимый эндпоинт)
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.memories[user_id][-50:]  # Ограничиваем историю
            ],
            api_key=self.api_key,
            api_base="https://api.deepseek.com/v1"
        )
        answer = response.choices[0].message.content
        self.memories[user_id].append({"role": "assistant", "content": answer})
        return answer
