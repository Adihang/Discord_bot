import discord
from discord.ext import commands
from MessegeDef import MessageDef
from sqlconnect import SQLConnect
from OpenAi import OpenAi

#MSSQLServer 에서 토큰 가져오기
SQLConnect = SQLConnect()
HB_TOKEN = SQLConnect.get_token("HB")
TOKEN = HB_TOKEN[0]
CHANNEL_ID = HB_TOKEN[1]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#봇이 켜졌을 때
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="MS AI School"))

#봇이 메세지를 읽었을 때
@bot.event
async def on_message(message):

    #봇이 자신의 메세지를 무시
    if message.author == bot.user:
        return

    #!로 시작하는 메세지를 읽으면
    if message.content.startswith('!'):
        rowMes = message.content.replace('!', '', 1)
        message_def = MessageDef()
        if rowMes.find("ai ") == 0:
            ai = OpenAi()
            rowMes = rowMes.replace('ai ', '', 1)
            if rowMes.find("코드리뷰") == 0:
                rowMes = rowMes.replace('코드리뷰', '', 1)
                print("코드리뷰 요청: " + rowMes)
                await message.channel.send(ai.code_review(rowMes))
            
        if rowMes.find("오늘의 문제") == 0:
            description, quizlist =  message_def.todayQuiz()
            await message.channel.send(description)
            for quiz in quizlist:
                msg = await message.channel.send(quiz)
                await msg.add_reaction("⬆️")
                await msg.add_reaction("👍")
                await msg.add_reaction("⬇️")

    await bot.process_commands(message)

bot.run(TOKEN)

# 디스코드 봇이 읽어온 메시지는 message 변수에 저장됩니다. on_message 이벤트 핸들러 함수에서 message 매개변수는 봇이 수신한 각 메시지를 나타냅니다.

# message 객체는 discord.Message 클래스의 인스턴스로, 메시지의 다양한 속성과 메서드를 사용하여 해당 메시지의 내용, 작성자, 채널 등의 정보에 접근할 수 있습니다. 명령어를 처리하거나 메시지에 응답하는 데 사용할 수 있는 유용한 기능을 제공합니다.

# 예를 들어, message.content 속성은 메시지의 내용을 문자열로 가져올 수 있습니다. message.author 속성은 메시지를 작성한 사용자를 나타내는 discord.Member 객체를 반환합니다. 또한, message.channel 속성은 메시지가 속한 채널을 나타내는 discord.TextChannel 객체를 반환합니다.

# message 객체의 다양한 속성과 메서드를 활용하여 메시지를 읽고 처리하는 로직을 구현할 수 있습니다.

