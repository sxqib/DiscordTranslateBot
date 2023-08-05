import discord
import os
import asyncio
import aiofiles
import json
import platform
import psutil
import openai
import io
import tiktoken
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
openai.api_key = os.getenv('OPENAI_API_KEY')


class OpenAITranslate:
    def __str__(self):
        return "OpenAI"
    
async def openai_translate(text, source_language, target_language, model, fallback_model):
    prompt = "You are now an advanced translator, your role is to provide translations that mirror the fluency and subtleties of a native speaker. You have the capability to handle a wide range of languages, You can also accept unique and entertaining translation styles to translate into which are provided by the user, such as UwU. Your responses should be strictly confined to the translated text, without any additional or extraneous content."
    
    temperature = 0
    
    if model == "gpt-4":
        max_tokens = 6000
        max_limit = 8192
    else:
        max_tokens = 3000
        max_limit = 4097
    
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Translate the following text: '{text}', from the source language: '{source_language}', into the target language: '{target_language}'"}
    ]
    
    try:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(prompt))
        if (num_tokens + max_tokens) > max_limit:
            raise ValueError(
                "Your text is too long! "
            )
        
        response = await openai.ChatCompletion.acreate(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages
        )

        translation = response['choices'][0]['message']['content']
    except:
        encoding = tiktoken.encoding_for_model(fallback_model)
        num_tokens = len(encoding.encode(prompt))
        if (num_tokens + max_tokens) > max_limit:
            raise ValueError(
                "Your text is too long! "
            )
        
        response = await openai.ChatCompletion.acreate(
            model=fallback_model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages
        )

        translation = response['choices'][0]['message']['content']
    
    return translation

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
        await bot.change_presence(activity=discord.Game(name="community server: https://discord.gg/j72z3jsZS3"), status=Status.idle)
        await asyncio.sleep(60)

async def fetch_translator(user_id):
    async with aiofiles.open('./JSONsDir/translators.json', 'r') as f:
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
async def translate(ctx, text: str = None, from_lang: str = None, to_lang: str = None, file: discord.Attachment = None):
    if not ((text or file) and from_lang and to_lang):
        embed = discord.Embed(
            title="❌ Missing Parameters!",
            description="Parameters (text or file, from_lang, and to_lang) are required!",
            color=discord.Colour.red(),
        )
        embed.add_field(name="Tip:", value="If you're using a .txt file, make sure you uploaded it.", inline=False)
        embed.set_footer(text="Made by TranslatorBot team.")
        await ctx.respond(embed=embed, ephemeral=True)
        return
    
    if file:
        # check if file is .txt
        if file.filename.split('.')[-1] != 'txt':
            embed = discord.Embed(
                title="❌ Invalid File!",
                description="File must be a .txt file!",
                color=discord.Colour.red(),
            )
            embed.set_footer(text="Made by TranslatorBot team.")
            await ctx.respond(embed=embed, ephemeral=True)
            return
        # read the file contents without downloading and save it to text
        text = await file.read()
        text = text.decode('utf-8')

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
            try:
                translated_text = await openai_translate(text, from_lang, to_lang, "gpt-4", "gpt-3.5-turbo")
            except Exception as E:
                if "Your text is too long!" in str(E):
                    embed4 = discord.Embed(
                        title="❌ An error occured!",
                        description="Your text is too long to translate!",
                        color=discord.Colour.red(),
                    )
                    embed4.set_footer(text="Made by TranslatorBot team.")

                    await ctx.respond(embed=embed4, ephemeral=True)
                    return
                else:
                # Fallback to DeeplTranslate telling that it has been fallbacked
                    embed1 = discord.Embed(
                        title="Fallbacked to DeeplTranslate!",
                        description="An error occured while translating the text using OpenAI, translation will be done using Deepl",
                        color=discord.Colour.orange(),
                    )
                    embed1.set_footer(text="Made by TranslatorBot team.")

                    await ctx.respond(embed=embed1, ephemeral=True)

                    translator = DeeplTranslate()
                    translated_text = await translatefunc(loop, text, from_lang, to_lang, translator)
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

    original_text = text
    if len(original_text) > 900:
        original_text = "The original text is too long to display here."

    if len(translated_text) > 900:
        result_text = "The translated text is too long to display here. Please check the attached txt file for the full translation."
        # Create a discord.File object with the contents of the translation
        file = discord.File(io.StringIO(f"Original Text:\n\n{text}\n\n\n\nTranslated Text:\n\n{translated_text}"), filename="translation.txt")
    else:
        result_text = "Your translated text is: " + str(translated_text)
        file = None

    embed3 = discord.Embed(
        title="✅ We do have results!",
        description="Your text was translated! The config and the text are below:",
        color=discord.Colour.green(),
    )
    embed3.add_field(name="Text language", value="Your text language: " + str(from_lang), inline=False)
    embed3.add_field(name="Target language", value="Your text target language: " + str(to_lang), inline=False)
    embed3.add_field(name="Service used", value=str(translator) + " Translate", inline=False)
    embed3.add_field(name="Original text", value=original_text, inline=False)
    embed3.add_field(name="Result Text", value=result_text, inline=False)
    embed3.set_footer(text=f"Made by TranslatorBot team. Request by {ctx.author.name}.") 

    await ctx.send(content=ctx.author.mention, embed=embed3, file=file)

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
    async with aiofiles.open('./JSONsDir/translators.json', 'r') as f:
        translators = await f.read()
    translators = json.loads(translators)
    
    translators[str(ctx.author.id)] = service
    
    async with aiofiles.open('./JSONsDir/translators.json', 'w') as f:
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
    async with aiofiles.open('./JSONsDir/avaliable.json', 'r') as f:
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
