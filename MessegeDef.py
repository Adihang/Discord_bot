from datetime import datetime
from sqlconnect import SQLConnect

class MessageDef:
    
    #오늘의 퀴즈 가져오기
    def todayQuiz(self):
        if datetime.now().weekday() >= 5:
            todayQuiz = "오늘은 휴일입니다.\n코딩에는 체력도 중요하니 밖에 나가서 운동을 해보는건 어떨까요?"
        else:
            SqlConnect = SQLConnect()
            todayQuiz = "# 오늘의 문제입니다!\n- 사용 언어는 **JavaScript** 또는 **Python**입니다.\n- 문제를 해결하고 자신의 코드를 '이름_문제이름'로 저장해 PR 해보세요!\n"
            today = str(datetime.now().strftime("%Y%m%d"))
            today_quiz_DB = SqlConnect.get_day_quiz(today)
            for i in today_quiz_DB:
                todayQuiz += i[1] + "\n" + "https://www.acmicpc.net/problem/" + str(i[0]) + "\n"
        print("todayQuiz:", todayQuiz)
        return todayQuiz