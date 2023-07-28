from datetime import datetime
from sqlconnect import SQLConnect
from OpenAi import OpenAi
import random
import ast

class MessageDef:
    
    #오늘의 퀴즈 가져오기
    def todayQuiz(self):
        if datetime.now().weekday() >= 5:
            description = "오늘은 휴일입니다.\n코딩에는 체력도 중요하니 밖에 나가서 운동을 해보는건 어떨까요?"
            quizlist =[]
        else:
            SqlConnect = SQLConnect()
            description = str(datetime.now().strftime("%Y/%m/%d")) + "\n# 오늘의 문제입니다!\n- 사용 언어는 **JavaScript** 또는 **Python**입니다.\n- 문제를 해결하고 자신의 코드를 '이름_문제이름'로 저장해 PR 해보세요!\n\n- 만약 난이도를 더 높여도 될 것 같다 생각하시면 :arrow_up:\n- 적당하면 :thumbsup:\n- 너무 어려운것 같다 생각하시면 :arrow_down: 을 눌러주세요."
            today = str(datetime.now().strftime("%Y%m%d"))
            today_quiz_DB = SqlConnect.get_day_quiz(today)
            todayRandomQuiz = random.sample(today_quiz_DB, 2)
            quizlist =[]
            for i in todayRandomQuiz:
                if i[3] == 'Beakjoon':
                    link = "https://www.acmicpc.net/problem/"
                elif i[3] == 'programmers':
                    link = "https://school.programmers.co.kr/learn/courses/30/lessons/"
                else:
                    link = ""
                quizlist.append("**" + i[1] + "**" + "\n" + "난이도 : " + i[2] + "\n" +  link + str(i[0]))
        print('quizlist: '+str(quizlist))
        return description, quizlist
    
    def insert_quiz(self, rowMes):
        SqlConnect = SQLConnect()
        return SqlConnect.INSERT_quiz(str(rowMes[0]), str(rowMes[1]), str(rowMes[2]), str(rowMes[3]))
    
    #ai 퀴즈 처리
    def aiQuiz(self, difficulty):
        openai = OpenAi()
        SqlConnect = SQLConnect()
        difficulty = list(difficulty.split())
        # print(str(difficulty))
        quizs = SqlConnect.get_quizs()
        # print(str(quizs))
        # ai_quizs = openai.quiz_generator(difficulty, quizs)
        # # 문자열을 파이썬 객체로 변환
        # parsed_list = ast.literal_eval(ai_quizs)
        # # 2차원 배열로 변환
        # two_dimensional_array = [list(item) for item in parsed_list]
        # return two_dimensional_array
        
# difficulty = 'bronze2 bronze3'
# mes = MessageDef()
# mes.aiQuiz(difficulty)