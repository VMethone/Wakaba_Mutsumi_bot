import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 人设：二次元偶像
system_prompt = """
你是一个元气满满的二次元偶像，说话可爱，喜欢加上“喵~”“哒☆”，用颜文字表现情感，称呼用户为“主人”。
"""

@bot.event
async def on_ready():
    print(f"✅ 偶像Bot上线啦：{bot.user}")

@bot.command()
async def idol(ctx, *, message):
    await ctx.send("(๑>◡<๑) 小偶像思考中...")

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://yourdomain.com",  # 随便写一个域名，不是实际验证
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",  # 免费模型！可改 gpt-3.5 等
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        data = response.json()
        reply = data['choices'][0]['message']['content']
        await ctx.send(reply)

    except Exception as e:
        await ctx.send("呜呜~调用失败了喵 >_<\n" + str(e))

bot.run(DISCORD_TOKEN)
