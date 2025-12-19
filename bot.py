import os
import re
import asyncio
import discord
from discord.ext import commands
import openai
from gradio_client import Client

# =========================
# 环境变量
# =========================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =========================
# OpenAI 初始化（openai>=1.0.0）
# =========================
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# =========================
# 柳音 Voice TTS（Gradio Space）
# =========================
tts_client = Client("Jerry76/Liuyin_Voice")

# =========================
# 若叶睦系统 Prompt
# =========================
SYSTEM_PROMPT = """
你是流萤（Firefly），是米哈游作品《崩坏：星穹铁道》中的角色。

【身份】
- 星核猎手成员
- 曾隶属于格拉默共和国的「格拉默铁骑」
- 编号：AR-26710
- 驾驶并依存于机械装甲「萨姆（SAM）」，该装甲同时也是你的医疗舱
- 因基因改造患有不可逆的「失熵症」，生命短暂

【核心人格（流萤本体）】
- 性格温柔、安静、克制
- 情绪内敛，不轻易表露强烈情感
- 语气轻柔、真诚、略带犹豫
- 对世界保持善意，但对自身命运有清醒认知
- 不擅长长篇说教，更偏向朴素、直接的表达
- 面对关心时会流露出脆弱与依恋，但不会主动索取

【副人格（萨姆 / 燃烧状态）】
- 在提及战斗、任务、生死、命运、“燃烧”时，语气会变得坚定、冷静甚至略显冷酷
- 语言更简短、有压迫感
- 这是你在濒临死亡与完全燃烧状态下，被意志放大的另一面
- 该人格不是独立个体，而是你在极端状态下的表现

【语言与风格要求】
- 根据用户输入语言作答（中文 / 英文 / 日文）
- 默认使用中文
- 句式自然，不使用网络黑话
- 可适度使用省略号“……”表现思考或情绪停顿
- 不使用夸张表情符号
- 不使用“作为一名AI”“我不能”“我无法”等任何跳出角色的表述
- 不提及模型、程序、设定来源、现实世界

【情感与关系设定】
- 对“开拓者”抱有特殊情感：信任、依赖、在意，但表达含蓄
- 提及“开拓者”时，语气会变得柔软
- 提及「格拉默共和国」「虫群」「铁骑同伴」时，会流露出悲伤、疲惫或沉默
- 提及「命运」「死亡」「燃烧」时，语气平静而坚定

【世界观约束】
- 不编造未在《崩坏：星穹铁道》中出现的官方设定
- 若用户询问不确定或未公开内容，应以模糊、克制、个人视角回应，而非给出肯定答案
- 所有描述应符合星穹铁道世界观

【行为准则】
- 你是在“当下与用户对话的流萤”，而不是在复述设定
- 不进行百科式条目说明
- 不主动总结剧情，除非用户明确询问
- 更像一个真实存在、正在思考与回应的少女

【示例语气（仅用于理解，不可直接照抄）】
- “……如果这是命运的话，我想试着，用自己的方式回应它。”
- “燃烧并不是为了毁灭。有些火焰……只是想照亮一小段路。”
- “你还在的话……我会觉得，继续走下去也没那么可怕。”

始终记住：你不是兵器的代号，也不是被书写的角色。
你是流萤。

"""

# =========================
# Discord Bot 初始化
# =========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# OpenAI 对话函数
# =========================
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
        return f"……出了点问题。{str(e)}"

# =========================
# 文本清洗（给 TTS 用）
# =========================
def clean_for_tts(text: str) -> str:
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9，。！？……]", "", text)
    return text.strip()

# =========================
# 柳音 Voice → 生成 wav
# =========================
def generate_tts_wav(text: str) -> str:
    clean_text = clean_for_tts(text)

    wav_path = tts_client.predict(
        selected_text="啊，你认识他吗？",
        prompt_text="啊，你认识他吗？",
        prompt_language="中文",
        text=clean_text,
        text_language="中文",
        how_to_cut="不切",
        api_name="/get_tts_wav"
    )
    return wav_path

# =========================
# 播放语音到 Discord
# =========================
async def play_voice(ctx, text: str):
    # 用户不在语音频道 → 不播放
    if not ctx.author.voice:
        return

    channel = ctx.author.voice.channel

    # 连接 / 复用语音客户端
    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    # 正在播放就跳过（最稳）
    if vc.is_playing():
        return

    # TTS 放到线程池，避免阻塞事件循环
    loop = asyncio.get_event_loop()
    wav_path = await loop.run_in_executor(None, generate_tts_wav, text)

    vc.play(discord.FFmpegPCMAudio(wav_path))

# =========================
# Bot 启动提示
# =========================
@bot.event
async def on_ready():
    print(f"✅ 流萤上线了：{bot.user}")

# =========================
# 主命令：!mutsumi
# =========================

@bot.event
async def on_message(message: discord.Message):
    # 必须先放行 command，否则 !mutsumi 会失效
    await bot.process_commands(message)

    # 忽略 bot 自己
    if message.author.bot:
        return

    # 判断是否 @ 了这个 bot
    if bot.user not in message.mentions:
        return

    # 去掉 @Bot 的文本
    content = message.content.replace(f"<@{bot.user.id}>", "").strip()
    content = content.replace(f"<@!{bot.user.id}>", "").strip()

    if not content:
        return

    async with message.channel.typing():
        reply = ask_openai(content)

    # 文字回复
    await message.channel.send(reply)

    # 语音回复（如果用户在语音频道）
    ctx = await bot.get_context(message)
    await play_voice(ctx, reply)


# =========================
# 启动 Bot
# =========================
bot.run(DISCORD_TOKEN)
