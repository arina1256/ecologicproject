import asyncio
import discord
import random
from discord.ext import commands
import os
from cl_model import get_class
from settings import TOKEN
from random import choice


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
#, help_command=None
async def send_message_by_symbols(message, text):
    msg = ''
    for i in range(len(text)):
        if not msg:
            msg = await message.channel.send(text[:i+1])
            continue

        await msg.edit(content=text[:i+1])

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')


@bot.command()
async def location(ctx):
    with open('images/ecopoints.png', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command('eco')
async def eco(ctx):
    eco_str = '''Экология - это наука, которая изучает взаимодействие живых организмов между собой и с окружающей средой. 
    Цель экологии - сохранение биологического видообразия и поддержание экосистем в равновесном состоянии. 
    Мы должны заботиться о природе и экологически устойчивом развитии, чтобы не нарушать баланс в природе.
    '''
    await ctx.send(eco_str)

@bot.command('hello')
async def hello(ctx):
    hello_str = '''Привет!Я - ecobot. Ты можешь написать '$helpMe', чтобы узнать какие команды у меня есть.
    '''
    await ctx.send(hello_str)

@bot.command('helpMe')
async def helpMe(ctx):
    helpMe_str = '''
      $hello поздороваться с ботом
      $advice получить совет от бота, чтобы уменьшить количество отходов
      $eco узнать об экологии
      $location узнать местонахождение Экопунктов
      если вы пришлете фото, то бот определит класс отходов
    '''
    await ctx.send(helpMe_str)

@bot.command('advice')
async def advice(ctx):
    await ctx.send(random.choice(["откажитесь от лишнего и отдайте эти вещи другим.","Сократите отходы там, где возможно","Используйте вещи повторно","Сортируйте отходы и сдавайте их на переработку","Компостируйте органический мусор","Используйте многоразовую посуду вместо пластиковой","Используйте шопперы вместо пакетов"]))

@bot.event
async def on_message(message):
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                message_for_user = await message.channel.send('Ваш файл обрабатывается. Подождите')
                file_name = attachment.filename
                image_path = f'images/{file_name}'
                await attachment.save(image_path)
                trash_name, score = get_class(model_path="model/keras_model.h5", labels_path="model/labels.txt", image_path=image_path)
                await message_for_user.delete()
                # await message.channel.send(f'Данные отходы относятся к классу {trash_name} с вероятностью {score}%')
                await send_message_by_symbols(message, f'Данные отходы относятся к классу {trash_name} с вероятностью {score}%')
                os.remove(image_path)
    await bot.process_commands(message)
bot.run(TOKEN)
