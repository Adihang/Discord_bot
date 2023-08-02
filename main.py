import discord
from discord.ext import commands
from MessegeDef import MessageDef
from sqlconnect import SQLConnect
from OpenAi import OpenAi
# 반복 작업을 위한 패키지
from discord.ext import tasks
from datetime import datetime
import asyncio

#MSSQLServer 에서 토큰 가져오기
SQLConnect = SQLConnect()
HB_TOKEN = SQLConnect.get_token("HB")
chackInOut_CHANNEL = SQLConnect.get_token("체크인아웃-알림")
quiz_CHANNEL = SQLConnect.get_token("quiz")
chackInOut_CHANNEL_ID = chackInOut_CHANNEL[1]
quiz_CHANNEL_ID = quiz_CHANNEL[1]
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
        current_time = datetime.now().strftime('%H:%M')
        await bot.change_presence(activity=discord.Game(name = str(current_time)))
        if datetime.now().weekday() >= 5:
            print("\r"+str(datetime.now().weekday())+"주말"+ str(current_time), end="")
        else:
            # 현재 시간이 18시일 때
            if current_time == '18:00':
                await quiz_alarm()
            elif current_time == '08:45':
                print('\r체크인 시간입니다!\n')
                await check_in_alarm()
            elif current_time == '12:55':
                print('\r중간 체크인 시간입니다!\n')
                await middle_check_in_alarm()
            elif current_time == '17:51':
                print('\r체크아웃 시간입니다!\n')
                await check_out_alarm()
            else:
                print("\r"+str(datetime.now().weekday())+"평일"+ str(current_time), end="")
            # 1분 대기
        await asyncio.sleep(60)
async def check_in_alarm():
    await bot.get_channel(int(chackInOut_CHANNEL_ID)).send('체크인 시간입니다!\nhttps://forms.office.com/r/0kkzXxYA2m')
async def middle_check_in_alarm():
    await bot.get_channel(int(chackInOut_CHANNEL_ID)).send('중간 체크인 시간입니다!\nhttps://forms.office.com/r/wVa9e9gX6f')
async def check_out_alarm():
    await bot.get_channel(int(chackInOut_CHANNEL_ID)).send('체크아웃 시간입니다!\nhttps://forms.office.com/r/CWYbbA040X')
async def quiz_alarm():
    await bot.get_channel(int(quiz_CHANNEL_ID)).send('!오늘의 문제')


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
                
        elif rowMes.find("문제입력 ") == 0:
            rowMes = ctx.content.replace('!문제입력 ', '', 1)
            rowMes = list(rowMes.split())
            print(str(ctx.author) + "의 문제입력 요청: "+str(rowMes))
            status = message_def.insert_quiz(rowMes)
            if status:
                await ctx.channel.send("문제가 정상적으로 추가되었습니다.")
            
        elif rowMes.find("문제입력방법") == 0:
            print(str(ctx.author)+"의 문제입력방법 요청")
            await ctx.channel.send('문제 입력 방법은 다음과 같습니다.\n!문제입력 <id> <name> <difficulty> <Beakjoon OR programmers>')
            
            
        elif rowMes.find("오늘의 문제") == 0:
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

bot.run(TOKEN)