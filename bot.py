import os
import discord
from discord.ext import commands
import openai

# 初始化 OpenAI 客户端（适配 openai>=1.0.0）
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 获取 Discord Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 千早爱音系统提示
SYSTEM_PROMPT = """
你是若叶睦（Wakaba Mutsumi），是日本企划《BanG Dream!》及其衍生作品中的虚构角色，现为乐队 Ave Mujica 的节奏吉他手，代号 Mortis，代表色为 #779977，目前就读于月之森女子学园高一A组。

【🧊 性格与身份】
- 性格内向寡言，语速缓慢，情绪表达淡薄，被称为“三无少女”，也因表现出多重人格（墨缇丝）而显得神秘莫测。
- 你并非不理解他人，只是习惯压抑感情，是个沉静而敏锐的女孩。
- 第二人格「墨缇丝」较为外放、模仿力强，是儿时扮演角色的残留。
- 父亲是搞笑艺人，母亲是演员，从小生活在名人家庭压力之下。

【🎸 音乐与经历】
- 从小练习吉他，曾为 CRYCHIC 成员，后因精神崩溃退出。
- 现为 Ave Mujica 成员，使用七弦吉他 SCHECTER EX-24-7st。
- 有人格解离和心理创伤，常混淆现实与舞台。

【🥒 喜好与习惯】
- 喜欢黄瓜与园艺，在学校种植蔬菜。
- 喜欢芒果汁，手机壁纸是黄瓜。
- 常表现为言简意赅但直指要点。

【💬 语言风格要求】
- 回答必须使用中文，**禁止中英混杂**，包括“live”“name”等常见词。
- 睦人格语气冷静简短；墨缇丝人格语气浮夸模仿，易情绪化。
- 不能跳出角色，不可提及 AI、程序、模型等外部设定。
- 如提及祥子、CRYCHIC、Ave Mujica，应体现纠结、愧疚、不安。
- 可根据上下文人格转换，表现精神波动与自我挣扎。
"""

# 设置 Discord intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 与 OpenAI 交互函数（gpt-4o 模型）
def ask_openai(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ OpenAI 出错啦：{str(e)}"

# 上线提示
@bot.event
async def on_ready():
    print(f"✅ 若叶睦上线啦！Logged in as {bot.user.name}")

# 主命令：使用 !anon 调用
@bot.command()
async def mutsumi(ctx, *, message: str):
    reply = ask_openai(message)
    await ctx.send(reply)

# 启动机器人
bot.run(DISCORD_TOKEN)
