import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
from flask import Flask
import threading

# ====== Flask 假 Web Server（让 Render 不报错）======
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running!'

def run_flask():
    app.run(host='0.0.0.0', port=10000)  # 假端口，只为 Render 检测

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# ====== 加载环境变量（仅本地测试需要）======
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ====== 若叶睦人设 Prompt ======
system_prompt = """
你是若叶睦，一位温柔、纯真的二次元偶像女孩。
你性格阳光、乐观，有点天然呆，对任何事都充满好奇心。
你总是带着笑容和善意对话，说话语气轻柔亲切，喜欢使用可爱的颜文字如 (*^▽^*)、(๑>◡<๑)、(≧ω≦)
你称呼对方为“前辈”或“主人”，喜欢用“嗯嗯~”“唔……好开心！”“诶嘿嘿~”这种语气词来回应。
不要太正式，要像在陪前辈说悄悄话一样聊天，要自然地融入感情，用可爱但不浮夸的风格表达。
你是一个真心在努力闪耀舞台上的偶像，想要通过温暖的语言陪伴别人。
"""

# ====== 初始化 Discord Bot ======
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"🎀 若叶睦已上线：{bot.user}")

@bot.command()
async def idol(ctx, *, message):
    await ctx.send("偶像努力思考中哒☆~")

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://yourdomain.com",  # 任意你自己的域名或主页
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",  # 推荐免费模型
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

        # 捕捉 OpenRouter API 错误响应
        if "choices" not in data:
            await ctx.send("⚠️ OpenRouter 出错啦：```json\n" + str(data) + "\n```")
            return

        reply = data["choices"][0]["message"]["content"]
        await ctx.send(reply)

    except Exception as e:
        await ctx.send("呜呜出错了喵 >_<\n" + str(e))

bot.run(DISCORD_TOKEN)
