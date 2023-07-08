import pymssql
import os
import json

class SQLConnect:
    def __init__(self):
        # mssql 접속정보 가져오기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mssql_config_file_path = os.path.join(script_dir, "mssql_config.json")
        with open(mssql_config_file_path, "r", encoding="utf-8") as mssql_config_file:
            mssql_config_data = json.load(mssql_config_file)
            
        server = mssql_config_data["server"]
        #port = mssql_config_data["port"]
        username = mssql_config_data["username"]
        password = mssql_config_data["password"]
        database = mssql_config_data["database"]

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
        self.cursor.execute("SELECT TOKEN, CHANNEL_ID FROM token WHERE name = '{}'".format(ID))
        result = self.cursor.fetchone()

        if result:
            token = result[0]
            channel_id = result[1]
            print(f"TOKEN: {token}\nCHANNEL_ID: {channel_id}")
            return result
        else:
            print("get_token : 해당하는 ID를 찾을 수 없습니다.")

    def get_day_quiz(self, date):
        self.cursor.execute("SELECT id, CAST(name AS NVARCHAR), tier FROM quiz WHERE date = '{}'".format(date))
        result = self.cursor.fetchall()

        if result:
            print(result)
            return result
        else:
            print("get_day_quiz : 해당하는 날짜를 찾을 수 없습니다.")

