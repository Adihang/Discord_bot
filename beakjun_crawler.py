import requests
import json
from sqlconnect import SQLConnect

class Beakjun_Crawler:
    def __init__(self):
        self.SqlConnect = SQLConnect()
        
    def beakjun_quiz_info(self, quiz_num):
        problem_url = 'https://solved.ac/api/v3/search/problem?query='
        response = requests.get(problem_url + str(quiz_num), headers={"User-Agent": "Mozilla/5.0"})
        content_str = response.content.decode('utf-8')
        data = json.loads(content_str)
        try:
            problemId = data["items"][0]["problemId"]
            title_ko = data["items"][0]["titleKo"]
            level = data["items"][0]["level"]
            ko_tags = []
            en_tags = []
            for tag in data["items"][0]["tags"]:
                ko_tags.append(tag["displayNames"][0]["name"])
                en_tags.append(tag["displayNames"][1]["name"])
            return problemId, title_ko, level, ko_tags, en_tags
        except:
            return False
        
    def main(self):
        for i in range(1000, 30000):
            try:
                if self.beakjun_quiz_info(i) != False:
                    problemId, title_ko, level, ko_tags, en_tags = self.beakjun_quiz_info(i)
                    self.SqlConnect.INSERT_quiz_info(problemId, title_ko, level, ko_tags, en_tags)
            except:
                pass
                
            
beakjun_crawler = Beakjun_Crawler()
beakjun_crawler.main()