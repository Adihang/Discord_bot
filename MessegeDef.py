from datetime import datetime
from sqlconnect import SQLConnect
from OpenAi import OpenAi
import random
import discord
import ast

class MessageDef:
    #오늘의 퀴즈 가져오기
    def todayQuiz(self, level):
        if datetime.now().weekday() >= 5:
            embed = discord.Embed(title = "오늘은 휴일입니다.",
                                  description = "코딩에는 체력도 중요하니 밖에 나가서 운동을 해보는건 어떨까요?")
            quizlist =[]
        else:
            SqlConnect = SQLConnect()
            today = str(datetime.now().strftime("%Y%m%d"))
            today_quiz_DB = SqlConnect.get_day_quiz(today)
            if len(today_quiz_DB) >= 2:
                todayRandomQuiz = random.sample(today_quiz_DB, 2)
            elif len(today_quiz_DB) == 1:
                RandomQuiz = SqlConnect.get_random_quiz(level)
                if today_quiz_DB[0] == 'none':
                    todayRandomQuiz = random.sample(RandomQuiz, 2)
                else:
                    todayRandomQuiz = today_quiz_DB
                    todayRandomQuiz += random.sample(RandomQuiz, 1)
            
            embed = discord.Embed(title = "오늘의 문제입니다!",
                                  description = "- 사용 언어는 **JavaScript** 또는 **Python**입니다.\n- 문제를 해결하고 자신의 코드를 '이름_문제이름'로 저장해 PR 해보세요!\n\n- 만약 난이도를 더 높여도 될 것 같다 생각하시면 :arrow_up:\n- 적당하면 :thumbsup:\n- 너무 어려운것 같다 생각하시면 :arrow_down: 을 눌러주세요.")
            quizlist =[]
            for i in todayRandomQuiz:
                if len(i) == 4:
                    if i[3] == 'Beakjoon':
                        link = "https://www.acmicpc.net/problem/"
                    elif i[3] == 'programmers':
                        link = "https://school.programmers.co.kr/learn/courses/30/lessons/"
                    else:
                        link = ""
                else:
                    link = "https://www.acmicpc.net/problem/"
                quizlist.append("**" + i[1] + "**" + "\n" + "난이도 : " + i[2] + "\n" +  link + str(i[0]))
        print('quizlist: '+str(quizlist))
        return embed, quizlist
    
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
    
    def vote(self, levels, tags):
        
        tags = ['수학',
            '구현',
            '다이나믹 프로그래밍',
            '자료 구조',
            '그래프 이론',
            '그리디 알고리즘',
            '브루트포스 알고리즘',
            '문자열',
            '그래프 탐색',
            '정렬',
            '기하학',
            '트리',
            '정수론',
            '세그먼트 트리',
            '이분 탐색',
            '애드 혹',
            '너비 우선 탐색',
            '시뮬레이션',
            '사칙연산',
            '깊이 우선 탐색',
            '누적 합',
            '비트마스킹',
            '많은 조건 분기',
            '해 구성하기',
            '조합론',
            '백트래킹',
            '해시를 사용한 집합과 맵',
            '스위핑',
            '트리를 사용한 집합과 맵',
            '우선순위 큐',
            '트리에서의 다이나믹 프로그래밍',
            '분할 정복',
            '분리 집합',
            '비트필드를 이용한 다이나믹 프로그래밍',
            '소수 판정',
            '두 포인터',
            '스택',
            '파싱',
            '재귀']

        
# difficulty = 'bronze2 bronze3'
# mes = MessageDef()
# mes.aiQuiz(difficulty)