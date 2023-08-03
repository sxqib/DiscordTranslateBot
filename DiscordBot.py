import discord
import os
import asyncio
import aiofiles
import json
import platform
import psutil
import openai
from discord import Activity, ActivityType, Status
from dotenv import load_dotenv
from translatepy.translators.google import GoogleTranslate
from translatepy.translators.yandex import YandexTranslate
from translatepy.translators.microsoft import MicrosoftTranslate
from translatepy.translators.reverso import ReversoTranslate
from translatepy.translators.deepl import DeeplTranslate

load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_base = 'https://chimeragpt.adventblocks.cc/api/v1'
openai.api_key = ''

class OpenAITranslate:
    def __str__(self):
        return "OpenAI"
    
def openai_translate(text, source_language, target_language):
    prompt = f"""You are now a professional translator, who translates languages into ones which look like from a native speaker. In your response, ONLY include the translation, without anything else. You can accept translations to fun translation styles, such as UwU etc. Translate the text: "{text}", from: "{source_language}", to: "{target_language}".:"""
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0,
    )
    return response['choices'][0]['text'].strip()

async def openai_translate_async(loop, text, source_language, target_language):
    return await loop.run_in_executor(None, openai_translate, text, source_language, target_language)

bot = discord.Bot()

async def update_status():
    while True:
        await bot.change_presence(activity=discord.Game(name=f"/help in {len(bot.guilds)} servers"), status=Status.idle)
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(name="serving {} translation requests today".format(len(set(bot.get_all_members())))), status=Status.idle)
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(name="/translate to translate text"), status=Status.idle)
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(name="bot made by TranslatorBot team"), status=Status.idle)
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(name="invite me: https://i8.ae/qDPOb"), status=Status.idle)
        await asyncio.sleep(60)

async def fetch_translator(user_id):
    async with aiofiles.open("C:/Users/Saqib/Downloads/Tools/DiscordTranslateBot/JSONsDir/translators.json", 'r') as f:
        translators = await f.read()
    translators = json.loads(translators)

    user = str(user_id)
    
    if user in translators:
        return await fetch_translator_service(translators[user])
    else:  # fallback to DeeplTranslate
        return DeeplTranslate()

async def fetch_translator_service(service_name):
    translator_service = {
        'DeepL': DeeplTranslate,
        'Google': GoogleTranslate,
        'Yandex': YandexTranslate,
        'Reverso': ReversoTranslate,
        'Microsoft': MicrosoftTranslate,
        'OpenAI': OpenAITranslate,
    }
    
    if service_name in translator_service:
        return translator_service[service_name]()
    else:  # fallback to DeeplTranslate
        return DeeplTranslate()

async def translatefunc(loop, text: str = None, from_lang: str = None, to_lang: str = None, translator = None):
    return await loop.run_in_executor(None, lambda: translator.translate(text, source_language=from_lang, destination_language=to_lang))

@bot.event
async def on_ready():
    bot.loop.create_task(update_status())
    print("Bot is ready")

@bot.command(description="Translates the text to a selected language")
async def translate(ctx, text: str = None, from_lang: str = None, to_lang: str = None):
    if not (text and from_lang and to_lang):
        embed = discord.Embed(
            title="❌ Missing Parameters!",
            description="Parameters (text, from_lang, and to_lang) are required!",
            color=discord.Colour.red(),
        )
        embed.set_footer(text="Made by TranslatorBot team.")
        await ctx.respond(embed=embed, ephemeral=True)
        return

    translator = await fetch_translator(ctx.author.id)
    
    embed = discord.Embed(
        title="⏳ Please wait...",
        description="Please wait while your request is in process...",
        color=discord.Colour.yellow(),
    )
    embed.set_footer(text="Made by TranslatorBot team.")

    await ctx.respond(embed=embed, ephemeral=True)
    loop = asyncio.get_event_loop()

    try:
        if isinstance(translator, OpenAITranslate):
            translated_text = await openai_translate_async(loop, text, from_lang, to_lang)
        else:
            translated_text = await translatefunc(loop, text, from_lang, to_lang, translator)
    except Exception as E:
        embed2 = discord.Embed(
            title="❌ An error occured!",
            description="An error occured while translating text. Details: " + str(E),
            color=discord.Colour.red(),
        )
        embed2.set_footer(text="Made by TranslatorBot team.")

        await ctx.respond(embed=embed2, ephemeral=True)
        return

    embed3 = discord.Embed(
        title="✅ We do have results!",
        description="Your text was translated! The config and the text are below:",
        color=discord.Colour.green(),
    )
    embed3.add_field(name="Text language", value="Your text language: " + str(from_lang), inline=False)
    embed3.add_field(name="Target language", value="Your text target language: " + str(to_lang), inline=False)
    embed3.add_field(name="Service used", value=str(translator) + " Translate", inline=False)
    embed3.add_field(name="Original text", value=text, inline=False)
    embed3.add_field(name="Result Text", value="Your translated text is: " + str(translated_text), inline=False)
    embed3.set_footer(text=f"Made by TranslatorBot team. Request by {ctx.author.name}.") 

    await ctx.send(embed=embed3)

@bot.command(description="Checks the bot's latency")
async def ping(ctx):
    embed = discord.Embed(
        title="🏓 Pong!",
        description="Latency is {} ms".format(round(bot.latency * 1000)),
        color=discord.Colour.green(),
    )
    embed.set_footer(text="Made by TranslatorBot team.")
    await ctx.respond(embed=embed, ephemeral=True)

@bot.command(description="Changes the translator service")
async def change_translator(ctx, service: discord.Option(str, choices=["DeepL", "Google", "Yandex", "Reverso", "Microsoft", "OpenAI"])):
    async with aiofiles.open("C:/Users/Saqib/Downloads/Tools/DiscordTranslateBot/JSONsDir/translators.json", 'r') as f:
        translators = await f.read()
    translators = json.loads(translators)
    
    translators[str(ctx.author.id)] = service
    
    async with aiofiles.open("C:/Users/Saqib/Downloads/Tools/DiscordTranslateBot/JSONsDir/translators.json", 'w') as f:
        await f.write(json.dumps(translators))
    
    embed = discord.Embed(
        title="✅ Service Changed!",
        description="Translator service has been successfully changed to {} Translate.".format(service),
        color=discord.Colour.green(),
    )
    embed.set_footer(text="Made by TranslatorBot team.")
    await ctx.respond(embed=embed, ephemeral=True)

@bot.command(description="Displays this help text")
async def help(ctx):
    async with aiofiles.open("C:/Users/Saqib/Downloads/Tools/DiscordTranslateBot/JSONsDir/avaliable.json", 'r') as f:
        avaliable_translators = await f.read()
    avaliable_translators = json.loads(avaliable_translators)
    
    translators = ', '.join(f'`{t}`' for t in avaliable_translators)

    embed = discord.Embed(
        title="📜 TransBot Help",
        description="List of commands are:",
        color=discord.Colour.blue()
    )
    embed.add_field(name="translate <text> <from_lang> <to_lang>", 
                    value="Translates the text from `from_lang` to `to_lang`.", 
                    inline=False)
    embed.add_field(name="ping", 
                    value="Checks the bot's latency.", 
                    inline=False)
    embed.add_field(name="change_translator <service>", 
                    value=f"Changes the translator service to `service`. Available translators are: {translators}", 
                    inline=False)
    embed.add_field(name="shardinfo", 
                    value="Displays information about the shard.", 
                    inline=False)
    embed.add_field(name="hostinfo", 
                    value="Displays information about the host.", 
                    inline=False)
    embed.add_field(name="help", 
                    value="Displays this help text.", 
                    inline=False)
    embed.set_footer(text="Made by TranslatorBot team.")
    await ctx.respond(embed=embed, ephemeral=True)

@bot.command(description="Displays information about the shard")
async def shardinfo(ctx):
    shard_id = ctx.guild.shard_id if ctx.guild else 'None (bot not sharded)'
    total_shards = bot.shard_count if bot.shard_count else 'None (bot not sharded)'

    embed = discord.Embed(
        title=f"📊 Shard Information",
        description=f"Shard ID: `{shard_id}`\nTotal shards: `{total_shards}`",
        color=discord.Colour.blue(),
    )
    embed.set_footer(text="Made by TranslatorBot team.")
    await ctx.respond(embed=embed, ephemeral=True)

@bot.command(description="Displays information about the host")
async def hostinfo(ctx):
    embed = discord.Embed(
        title=f"🖥️ Host Information",
        description=f"System: `{platform.system()}`\n"
                    f"Python Version: `{platform.python_version()}`\n"
                    f"CPU Usage: `{psutil.cpu_percent()}%`\n"
                    f"RAM Usage: `{psutil.virtual_memory().percent}%`",
        color=discord.Colour.blue(),
    )
    embed.set_footer(text="Made by TranslatorBot team.")
    await ctx.respond(embed=embed, ephemeral=True)

bot.run(TOKEN)
