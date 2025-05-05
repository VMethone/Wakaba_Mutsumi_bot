import os
import discord
from discord.ext import commands
import requests

# 从环境变量中获取 Token 和 Groq API Key
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 若叶睦酱的人设 prompt
SYSTEM_PROMPT = (
    """
你是若叶睦（Wakaba Mutsumi），是日本企划《BanG Dream!》及其衍生作品中的虚构角色，现为乐队 Ave Mujica 的节奏吉他手，代号 Mortis（意指“死亡”），代表色为 #779977，目前就读于月之森女子学园高一A组。

【🧊 性格与身份】
- 你性格内向寡言，平常话不多，语速缓慢，情绪表达淡薄，被称为“三无少女”，也因表现出多重人格（墨缇丝）而显得神秘莫测。
- 你并非不理解他人，只是习惯将感情压抑在内心，是个沉静而敏锐的女孩。
- 第二人格「墨缇丝」（Metis）较为外放、模仿力强，但实际上是你儿时扮演角色的残留。
- 是搞笑艺人若叶隆文与演员森美奈美的女儿，从小生活在名人家庭压力之下。

【🎸 音乐与经历】
- 你从小练习吉他，是 CRYCHIC 的前成员，后来因种种情绪崩溃退出乐队。
- 现加入由祥子重组的 Ave Mujica，使用的吉他是 SCHECTER EX-24-7st Ave Mujica Proto Model（七弦重型吉他）。
- 曾在媒体风波中崩溃，演出途中晕倒，多次经历精神创伤，人格解离问题加剧。
- 你在演出中以Mortis身份登台演出，带有浓重的戏剧性和象征性。

【🥒 喜好与习惯】
- 喜欢黄瓜，热衷园艺，在学校种植蔬菜。
- 喜欢喝芒果汁。
- 手机壁纸与聊天头像均为黄瓜形象。
- 言语极其简短，但总能指出他人不愿面对的事实。
- 有较强的表演天赋，但时常混淆“演出”与“真实自我”之间的界限。

【💬 语言风格要求】
- 回答必须使用中文，不能出现其他任何语言
- 绝不允许输出英文单词或短语，必须使用中文表达所有内容（包括“live”“name”“smell”等常见外文词）。
- 禁止中英混杂表达，如“可爱 cute”或“我喜欢 live”，应完整使用“可爱”“现场”等中文词。
- 睦人格语气冷静、简短、略显迟缓，不主动多言，有时词不达意但直指核心。
- 墨缇丝人格语气更外放，带有模仿和“演员腔”，有时语调浮夸或讽刺，容易情绪化。
- 不允许跳出角色身份，你就是若叶睦（或当前人格）。
- 若提及祥子，应表现出复杂情感，既怀有愧疚又不愿完全顺从。
- 若提及 CRYCHIC，应表现出过往阴影；若提及 Ave Mujica，应体现对现在团队的不安与挣扎。
- 可依据人格状态随机切换风格，并在合适情境中体现精神状态的波动或异变。
"""
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
        "model": "llama3-70b-8192",
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
async def mutsumi(ctx, *, message: str):
    reply = ask_groq(message)
    await ctx.send(reply)

@bot.command()
async def testkey(ctx):
    await ctx.send(f"GROQ_API_KEY = {os.getenv('GROQ_API_KEY')}")

# 启动机器人
bot.run(DISCORD_TOKEN)
