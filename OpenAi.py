import openai
import os
import json

class OpenAi:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, "config.json")
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
        openai.api_key = str(config_data["OpenAI_API_Key"])
        print("OpenAI_API_Key: ", openai.api_key)
        
    def code_review(self, request):
        # 사용자 질문 입력
        prompt = request

        # 응답
        completion = openai.ChatCompletion.create(
            # 사용할 모델
            model="gpt-3.5-turbo",
            # 보낼 메세지 목록
            messages=[{"role": "system", "content":"You are a chatbot that does code reviews in Korean."},
                    {"role": "user", "content": prompt}]) # 사용자
        # 출력
        response = completion.choices[0].message.content
        return response