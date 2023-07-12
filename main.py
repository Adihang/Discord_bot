import discord
from discord.ext import commands
from MessegeDef import MessageDef
from sqlconnect import SQLConnect
from OpenAi import OpenAi
# 반복 작업을 위한 패키지
from discord.ext import tasks
# 현재 시간을 받아와 구조체에 넣어주는 용도로 사용할 패키지
import datetime
import asyncio

#MSSQLServer 에서 토큰 가져오기
SQLConnect = SQLConnect()
HB_TOKEN = SQLConnect.get_token("HB")
TOKEN = HB_TOKEN[0]
CHANNEL_ID = HB_TOKEN[1]
SERVER_ID = HB_TOKEN[2]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#봇이 켜졌을 때
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f"[!] 참가 중인 서버 : {len(bot.guilds)}개의 서버에 참여 중\n")
    await bot.change_presence(activity=discord.Game(name = str(len(bot.guilds))+"개의 서버에 참여"))
    
    # 18시에 메세지를 보내는 함수를 실행하는 루프 생성
    while True:
        # 현재 시간을 가져옴
        current_time = datetime.datetime.now().strftime('%H:%M')
        print("\r"+ str(current_time), end="")
        # 현재 시간이 18시일 때
        if current_time == '18:00':
            # 메세지를 보내는 함수 호출
            await quiz_alarm()
        # 1분 대기
        await asyncio.sleep(60)

#봇이 메세지를 읽었을 때
@bot.event
async def on_message(ctx):

    #봇이 자신의 메세지를 무시
    #if message.author == bot.user:
    #    return

    #!로 시작하는 메세지를 읽으면
    if ctx.content.startswith('!'):
        rowMes = ctx.content.replace('!', '', 1)
        message_def = MessageDef()
        
        if rowMes.find("ai ") == 0:
            ai = OpenAi()
            rowMes = rowMes.replace('ai ', '', 1)
            if rowMes.find("코드리뷰") == 0:
                rowMes = rowMes.replace('코드리뷰', '', 1)
                print(str(ctx.author)+"의 코드리뷰 요청: " + rowMes)
                await ctx.channel.send(ai.code_review(rowMes))
                
        if rowMes.find("문제입력") == 0:
            sql = SQLConnect()
            rowMes = ctx.content.replace('문제입력 ', '', 1)
            rowMes = list(rowMes.split())
            sql.insert_quiz(int(rowMes[0]), str(rowMes[1]), str(rowMes[2]))
            
            
        if rowMes.find("오늘의 문제") == 0:
            rowMes = ctx.content.replace('오늘의 문제', '', 1)
            #message_def.aiQuiz(rowMes)
            
            
            description, quizlist =  message_def.todayQuiz()
            await ctx.channel.send(description)
            if len(quizlist) > 0:
                for quiz in quizlist:
                    msg = await ctx.channel.send(quiz)
                    await msg.add_reaction("⬆️")
                    await msg.add_reaction("👍")
                    await msg.add_reaction("⬇️")
            print(str(ctx.author)+"의 오늘의 문제 요청: " + rowMes)
    await bot.process_commands(ctx)

async def quiz_alarm():
    await bot.get_channel(int(CHANNEL_ID)).send('!오늘의 문제')

bot.run(TOKEN)