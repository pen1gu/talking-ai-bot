import os
import sqlite3
from datetime import datetime
from pytz import timezone, utc
from discord import *
from discord.ext import commands
from sqlite3 import connect

client = Client()
prefix = '-'
# bot = commands.Bot(command_prefix='-', help_command=None)
conn = connect('db.sqlite3')


@client.event
async def on_ready():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS SERVER_TB
        (
            IDX        INTEGER     NOT NULL CONSTRAINT SERVER_TB_pk PRIMARY KEY AUTOINCREMENT,
            SERVER_ID  VARCHAR(20) NOT NULL,
            CHANNEL_ID VARCHAR(20) NULL DEFAULT NULL,
            CREATED_AT DATETIME NOT NULL,
            DELETED_AT DATETIME NULL DEFAULT NULL
        );
    """)
    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS SERVER_TB_SERVER_ID_uindex ON SERVER_TB (SERVER_ID);
    """)

    print('We have logged in as {0.user}'.format(client))

    await client.change_presence(status=Status.online, activity=Game(name='-help | 채팅 대기'))


@client.event
async def on_message(message):
    channel_id = conn.execute(
        'SELECT CHANNEL_ID FROM SERVER_TB WHERE SERVER_ID = "{}" AND DELETED_AT IS NULL'.format(
            str(message.guild.id))).fetchone()[0]

    if str(message.channel.id) == str(channel_id) and message.author != client.user and message.author.bot is not True:
        """
        받은 메세지 : message.content
        메세지 보내는 방법 : `await message.channel.send("보낼 메세지")` 
        """
        await message.channel.send("DETECTED CHANNEL!")

    if message.content.startswith('-init'):
        await init(message)

    if message.content.startswith('-help'):
        await help(message)


async def init(message):
    try:
        conn.execute(
            'INSERT INTO SERVER_TB (SERVER_ID, CREATED_AT) VALUES ("' + str(message.guild.id) + '", "' + str(
                utc.localize(
                    datetime.utcnow()).astimezone(timezone('Asia/Seoul'))) + '")')
        conn.commit()

        await message.guild.create_text_channel(name='gaon-channel')

        for channel in message.guild.text_channels:
            if channel.name == 'gaon-channel':
                conn.execute(
                    'UPDATE SERVER_TB SET CHANNEL_ID = "' + str(channel.id) + '" WHERE SERVER_ID = "' + str(
                        message.guild.id) + '"'
                )
                conn.commit()

        await message.channel.send('채팅 채널이 활성화되었습니다.')
    except sqlite3.IntegrityError:
        await message.channel.send('이미 채팅 채널이 존재합니다.')


async def help(message):
    embed = Embed(
        title='가온 사용자 매뉴얼',
        description='''
            디스코드에서 동작하는 당신만의 챗봇, 가온입니다.\n\n
            1. `-init` 명령어로 챗봇을 활성화합니다.\n\n
            2. `gaon-channel`이라는 **채팅 채널**이 생성됩니다.\n\n
            3. 해당 채널에서만 챗봇 이용이 가능합니다.
            '''
    )
    await message.channel.send(embed=embed)


client.run(os.environ.get('DISCORD_TOKEN'))
