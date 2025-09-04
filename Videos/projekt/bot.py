import discord
from discord.ext import commands
import json
import datetime
import os

#права для бота
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "!", intents=intents)

#чёт типа приветствия
@bot.event
async def on_ready():
    print(f'Bot {bot.user} ready for shit')
    await bot.change_presence(activity = discord.Game(name = "maybe help you"))

#ответ на васап
@bot.command()
async def hello(ctx):
    await ctx.send(
        f"wath's up {ctx.author.mention}, Комманды: !userinfo !admin !clean"
        )

#варны
def load_warns():
    try:
        with open('warns.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_warns(warns):
    with open('warns.json', 'w') as f:
        json.dump(warns, f, indent=4)

#команда варн
@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="Fuck server"):
    if member == ctx.author:
        await ctx.send("самого себя нельзя оклеветать")
        return
    if member.top_role >= ctx.author.top_role:
        await ctx.send("Нельзя оклеветать юзера из равной или высшей касты")
        return
    
    warns = load_warns()
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)

    if guild_id not in warns:
        warns[guild_id] = {}
    if user_id not in warns[guild_id]:
        warns[guild_id][user_id] = []

    warns[guild_id][user_id].append({
        "reason": reason,
        "moderator": ctx.author.id,
        "time": str(datetime.datetime.now())
    })

    save_warns(warns)
    await ctx.send(f"{member.mention} получил disrespec. Причина: {reason}")

#уведомление о варне
    try:
        await member.send(f"Вы получили disrespect на сервере **{ctx.guild.name}**\nПричина: {reason}")
    except:
        pass
#просмотр варнов
@bot.command()
async def warns(ctx, member: discord.Member = None):
    member = member or ctx.author
    warns = load_warns()
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)

    if guild_id not in warns or user_id not in warns[guild_id] or not warns[guild_id][user_id]:
        await ctx.send(f"У {member.mention} нет варнов.")
        return

    embed = discord.Embed(title=f"Disrespect {member.display_name}", color=0xff9900)
    for i, warn_data in enumerate(warns[guild_id][user_id], 1):
        moderator = await bot.fetch_user(warn_data["moderator"])
        embed.add_field(
            name=f"Disrespect #{i}",
            value=f"Причина: {warn_data['reason']}\nМодератор: {moderator.mention}\nВремя: {warn_data['time']}",
            inline=False
        )
    await ctx.send(embed=embed)


#автоудаление соощений
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clean(ctx, quantity: int = 10):
    await ctx.channel.purge(limit = quantity + 1)
    msg = await ctx.send(f"{quantity} сообщений удалено")
    await msg.delete(delay=5)

#userinfo
@bot.command()
async def userinfo(ctx, user: discord.Member = None):
    target = user or ctx.author
    if not target.joined_at:
        await ctx.send("Нету такого на сервере")
        return
    embed = discord.Embed(
        title=f"Профиль {target.display_name}",
        color=target.color
    )
    embed.set_thumbnail(url=target.avatar.url)
    embed.add_field(name="Присоеденился", value=target.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Аккаунт создан", value=target.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Статус", value=str(target.status).title(), inline=True)
    embed.add_field(name="Высшая роль", value=target.top_role.mention, inline=True)
    await ctx.send(embed=embed)

#приветствие нового юзера
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(
            f"Wasap, {member.mention}!\n"
            "Ознакомся с правилами мазафакер"
        )
    #присвоение касты 
    role = discord.utils.get(member.guild.roles, name="Простой работяга")
    if role:
        await member.add_roles(role)

#система каст
    
    #+опыт
#     add_xp(message.author.id, 20)
#     await bot.process_commands(message)

# #новая каста
# @bot.command()
# async def lwl(ctx):
#     xp = get_xp(ctx.author.id)
#     level = xp // 100
#     await ctx.send(f"Ты теперь в новой касте: {level} ({xp} XP)")

#admin
@bot.command()
async def admin(ctx):
    await ctx.send(f"Хел но, админу 9 годиков")

#авто-модерация

def load_bad_words():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'bad_words.txt')

    try:
        with open('bad_words.txt', 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("Файл bad_words.txt не найден! Создайте его с списком запрещенных слов.")
        return []
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    bad_words = load_bad_words()
    content = message.content.lower()

    #запретки
    for word in bad_words:
        if word in content:
            await message.delete()
            warning_msg = await message.channel.send(
                f"{message.author.mention}, за такие пантовые сообщения скоро будет бан"
                )
            await warning_msg.delete(delay=20)
            break
    
    #чтобы команды работали
    await bot.process_commands(message) 





@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Произошла внутренняя ошибка при выполнении команды")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Недостаточно прав для выполнения команды")

#мут
# Мут пользователя
@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: int = 20, *, reason="Не стоило разбрасыватья словами"):
    try:
        await member.timeout(datetime.timedelta(minutes=duration), reason=reason)
        await ctx.end(f"Суки за что мут {member.mention} на {duration} минут. Причина {reason}")
    except discord.Forbidden:
        await ctx.send("Для таких мувов нужна каста повыше")

#Размут
@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"Размутили {member.mention}")
    except discord.Forbidden:
        await ctx.send("Для таких мувов нужна каста повыше")

#токен который никому нельзя говорить
bot.run("MTQwMjI0NjQxNzQ1OTcwNzkxNg.GLBuJP.qsH7pHTa9EW1RLjLNV7ixFfacX-BFoh3hGazoY")