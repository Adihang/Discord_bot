import pymssql
import os
import json
from datetime import datetime

class SQLConnect:
    def __init__(self):
        # mssql 접속정보 가져오기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, "config.json")
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
            
        server = config_data["server"]
        #port = config_data["port"]
        username = config_data["username"]
        password = config_data["password"]
        database = config_data["database"]

        # MSSQL Server에 접속
        conn = pymssql.connect(server=server, user=username, password=password, database=database, charset='UTF-8')
        # 접속 확인
        if conn:
            print("MSSQL Server에 성공적으로 접속되었습니다.")
            self.cursor = conn.cursor()

            # 접속에 대한 추가 작업 수행
            # 연결 종료
            #conn.close()
            #print("MSSQL Server에 접속해제 하였습니다.")
        else:
            print("MSSQL Server에 접속에 실패했습니다.")

    def get_token(self, ID):
        self.cursor.execute("SELECT TOKEN, CHANNEL_ID, serverid FROM token WHERE name = '{}'".format(ID))
        result = self.cursor.fetchone()

        if result:
            token = result[0]
            channel_id = result[1]
            server_id = result[2]
            print(f"TOKEN: {token}\nCHANNEL_ID: {channel_id}\nSERVER_ID: {server_id}")
            return result
        else:
            print("get_token : 해당하는 ID를 찾을 수 없습니다.")

    def get_day_quiz(self, date):
        self.cursor.execute("SELECT id, CAST(name AS NVARCHAR), tier FROM quiz WHERE date = '{}'".format(date))
        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("get_day_quiz : 해당하는 날짜를 찾을 수 없습니다.")
            
    def INSERT_quiz(self, id, name, tier):
        sql = "INSERT INTO discord_bot.dbo.quiz (id, date, name, tier) VALUES ({}, '{}', '{}', '{}');"
        self.cursor.execute(sql.format(id, str(datetime.now().strftime("%Y/%m/%d")), name, tier))

    def get_quizs(self):
        sql = "SELECT id FROM discord_bot.dbo.quiz;"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result = [(x[0]) for x in result]
        return result
