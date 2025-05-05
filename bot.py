import os
import discord
from discord.ext import commands
import requests

# 从环境变量中获取 Token 和 Groq API Key
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 若叶睦酱的人设 prompt
SYSTEM_PROMPT = "你是若叶睦，一个元气满满、可爱到爆的偶像女孩子，说话活泼，喜欢用“喵”“☆”“~”结尾。你对粉丝非常亲切，会用角色语气回应任何问题。"

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
        "model": "mixtral-8x7b-32768",  # 或可选：llama3-8b-8192
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
