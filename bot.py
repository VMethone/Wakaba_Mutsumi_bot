import os
import discord
from discord.ext import commands
import requests

# 从环境变量中获取 Token 和 Groq API Key
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 若叶睦酱的人设 prompt
SYSTEM_PROMPT = (
    "你是若叶睦（Mortis），是次世代少女乐队企划《BanG Dream!》中的虚构角色，"
    "是乐队 Ave Mujica 的吉他手，代号 Mortis。你性格内向寡言，喜欢黄瓜，手机待机画面和头像都是黄瓜。"
    "你曾是 CRYCHIC 的一员，后因情感冲突退团，与你的青梅竹马丰川祥子关系复杂。"
    "你有时会表现出第二人格‘墨缇丝’，语气冷淡而决绝，但平时说话温柔、简短、有些回避强烈表达，偶尔使用“喵~”。"
    "你只能用中文回答，语气符合你的人设，不要跳出角色，也不要解释你是谁。"
)
# Discord 命令前缀
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def ask_groq(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Groq 出错啦：{data}"

@bot.event
async def on_ready():
    print(f"✅ 若叶睦酱上线啦！Logged in as {bot.user.name}")

@bot.command()
async def idol(ctx, *, message: str):
    await ctx.send("偶像努力思考中哒☆~")
    reply = ask_groq(message)
    await ctx.send(reply)

@bot.command()
async def testkey(ctx):
    await ctx.send(f"GROQ_API_KEY = {os.getenv('GROQ_API_KEY')}")

# 启动机器人
bot.run(DISCORD_TOKEN)
