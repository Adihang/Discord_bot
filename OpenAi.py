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
        self.memory_size = 5
        
    def code_review(self, request):
        # 사용자 질문 입력
        prompt = request

        # 응답
        completion = openai.ChatCompletion.create(
            # 사용할 모델
            model="gpt-3.5-turbo",
            # 보낼 메세지 목록
            messages=[
                #역할부여
                {"role": "system", "content":"You should do a code review. In Korean. " +
                 "possible that the user entered the code by wrapping it in ```. " +
                 "important!!! You need to add comments to user's code and wrap it with ```py and ``` important!!!. " +
                 "Since the conversation will only be exchanged once, you must complete all explanations at once."
                 },
                # 사용자
                {"role": "user", "content": prompt}
            ])
        # 출력
        response = completion.choices[0].message.content
        return response
    
    def quiz_generater(self, difficulty, solved_quiz):
        # 사용자 질문 입력
        prompt = request

        # 응답
        completion = openai.ChatCompletion.create(
            # 사용할 모델
            model="gpt-3.5-turbo",
            # 보낼 메세지 목록
            messages=[
                #역할부여
                {"role": "system", "content":"You are a chatbot that does code reviews in Korean. It is possible that the user entered the code by wrapping it in ```."},
                {"role": "user", "content": "difficulty: ['bronze2'], solved_quiz: [1012, 1018, 1065, 1259, 1316, 1966, 2444, 2577, 2579]"},
                {"role": "assistant", "content": "[[1978, '소수찾기']]"},
                {"role": "user", "content": "difficulty: ['bronze2', 'silver4'], solved_quiz: [1012, 1018, 1065, 1259, 1316, 1966, 2444, 2577, 2579]"},
                {"role": "assistant", "content": "[[1978, '소수찾기'], [9012, '괄호']]"},
                # 사용자
                {"role": "user", "content": prompt}
            ])
        # 출력
        response = completion.choices[0].message.content
        return response