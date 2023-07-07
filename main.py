import discord
from discord.ext import commands
from datetime import datetime
import json
import os

# 현재 스크립트의 디렉토리 경로
script_dir = os.path.dirname(os.path.abspath(__file__))

# JSON 파일 경로
config_file_path = os.path.join(script_dir, "config.json")
quiz_file_path = os.path.join(script_dir, "quiz.json")

# 토큰과 채널 아이디 가져오기
with open(config_file_path, "r", encoding="utf-8") as config_file:
    config_data = json.load(config_file)
TOKEN = config_data["TOKEN"]
print("TOKEN:", TOKEN)
CHANNEL_ID = config_data["CHANNEL_ID"]
print("CHANNEL_ID:", CHANNEL_ID)

#오늘의 퀴즈 가져오기
with open(quiz_file_path, "r", encoding="utf-8") as quiz_file:
    quiz_data = json.load(quiz_file)
todayQuiz = quiz_data[datetime.now().strftime("%Y%m%d")+"quiz"]
print("todayQuiz:", todayQuiz)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="MS AI School"))

@bot.event
async def on_message(message):

    #봇이 자신의 메세지를 무시
    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        rowMes = message.content.replace('!', '', 1)
        if rowMes == '오늘의 문제':
            await message.channel.send("# "+rowMes+"\n"+todayQuiz)

    await bot.process_commands(message)

bot.run(TOKEN)

# 디스코드 봇이 읽어온 메시지는 message 변수에 저장됩니다. on_message 이벤트 핸들러 함수에서 message 매개변수는 봇이 수신한 각 메시지를 나타냅니다.

# message 객체는 discord.Message 클래스의 인스턴스로, 메시지의 다양한 속성과 메서드를 사용하여 해당 메시지의 내용, 작성자, 채널 등의 정보에 접근할 수 있습니다. 명령어를 처리하거나 메시지에 응답하는 데 사용할 수 있는 유용한 기능을 제공합니다.

# 예를 들어, message.content 속성은 메시지의 내용을 문자열로 가져올 수 있습니다. message.author 속성은 메시지를 작성한 사용자를 나타내는 discord.Member 객체를 반환합니다. 또한, message.channel 속성은 메시지가 속한 채널을 나타내는 discord.TextChannel 객체를 반환합니다.

# message 객체의 다양한 속성과 메서드를 활용하여 메시지를 읽고 처리하는 로직을 구현할 수 있습니다.