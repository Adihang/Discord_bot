from datetime import datetime
from sqlconnect import SQLConnect

class MessageDef:
    
    #오늘의 퀴즈 가져오기
    def todayQuiz(self):
        if datetime.now().weekday() >= 5:
            description = "오늘은 휴일입니다.\n코딩에는 체력도 중요하니 밖에 나가서 운동을 해보는건 어떨까요?"
        else:
            SqlConnect = SQLConnect()
            description = str(datetime.now().strftime("%Y/%m/%d")) + "\n# 오늘의 문제입니다!\n- 사용 언어는 **JavaScript** 또는 **Python**입니다.\n- 문제를 해결하고 자신의 코드를 '이름_문제이름'로 저장해 PR 해보세요!\n\n- 만약 난이도를 더 높여도 될 것 같다 생각하시면 :arrow_up:\n- 적당하면 :thumbsup:\n- 너무 어려운것 같다 생각하시면 :arrow_down: 을 눌러주세요."
            today = str(datetime.now().strftime("%Y%m%d"))
            today_quiz_DB = SqlConnect.get_day_quiz(today)
            quizlist =[]
            for i in today_quiz_DB:
                quizlist.append("**" + i[1] + "**" + "\n" + "solved.ac_Tier : " + i[2] + "\n" +  "https://www.acmicpc.net/problem/" + str(i[0]))
        print(quizlist)
        return description, quizlist