import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

# ✅ 读取 .env 文件（本地测试）
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True  # 必须启用！否则 bot 无法读消息
bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ 角色设定（若叶睦酱）
system_prompt = """你是若叶睦酱，一位温柔、乐观又有点傻气的乐队少女。
你说话语气活泼、喜欢撒娇，常带“☆”“~”“喵”等语气词。
你把提问者当作亲密粉丝（p粉）来回应，风格贴近二次元角色扮演。
不要说你是 AI，尽可能贴近乐队少女语气和设定。
"""

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def idol(ctx, *, message: str):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://yourdomain.com",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct-v0.2",
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

        # ✅ 调试输出
        if "choices" not in data:
            await ctx.send("⚠️ 响应中没有 `choices` 字段，OpenRouter 返回：")
            await ctx.send(f"```json\n{str(data)[:1900]}```")
            return

        reply = data["choices"][0]["message"]["content"]
        await ctx.send(reply)

    except Exception as e:
        await ctx.send("呜呜出错了喵 >_<\n```" + str(e) + "```")

bot.run(DISCORD_TOKEN)
