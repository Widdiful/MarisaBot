import discord, random, asyncio, os, time, datetime, math, calendar, twitter, socket, re, ftputil
from discord.ext import commands
from threading import Thread
from time import sleep

description = '''I'm Marisa Kirisame! An ordinary magician!'''
bot = commands.Bot(command_prefix='!', description=description)
                  
ftpinfo = open('botinfo.txt').readlines()
for line in ftpinfo:
    line = line.replace("\r\n", "")
ipadr = ftpinfo[4].replace("\n", "")
user = ftpinfo[5].replace("\n", "")
passw = ftpinfo[6].replace("\n", "")
ftp = ftputil.FTPHost(ipadr, user, passw)

async def updateEmotes():
    ftp = ftputil.FTPHost(ipadr, user, passw)
    files = ftp.listdir('/emotes')
    emotes = os.listdir('emotes')
    for filename in os.listdir('emotes'):
        if filename not in files:
            if os.path.isfile('emotes/' + filename):
                print ("uploading " + filename)
                ftp.upload(os.path.join('emotes/', filename), os.path.join('/emotes/', filename))
    for filename in files:
        if filename not in emotes:
            ftp.remove(os.path.join('/emotes/', filename))

async def background_shit():
    await bot.wait_until_ready()
    print ('connected')
    while True:
        currentTime = datetime.datetime.now()
        
        reminders = []
        for line in open('text/reminders.txt').readlines():
            reminders.append(line.replace("\n", ""))
            
        nextReminderHour = int(reminders[0].split(':')[0])
        nextReminderMinute = int(reminders[0].split(' ')[0].split(':')[1])
        nextReminderChannel = reminders[0].split(' ')[1]
        nextReminderUser = reminders[0].split(' ')[2]
        nextReminderMessage = str('<@' + nextReminderUser + '> ' + reminders[0].split(' ', 3)[3])
        
        if (datetime.datetime.now().minute % 10 == 0):
            await updateEmotes()
        if (currentTime.minute == 0 and currentTime.hour == 0):
            gennames = open('general.txt').readlines()
            for line in gennames:
                line = line.replace("\r\n", "")
            general = bot.get_channel("123611091086475264")
            newgen = random.choice(gennames)
            while (newgen == general.name and newgen != "general"):
                newgen = random.choice(gennames)
            await bot.edit_channel(general, name = newgen)
            print("changed name to " + newgen)
                
            for server in bot.servers:
                for srole in server.roles:
                    if "340962768582868992" in srole.id:
                        names = open('names.txt').readlines()
                        for line in names:
                            line = line.replace("\r\n", "")
                        await bot.edit_role(server, srole, name = random.choice(names))
            await asyncio.sleep(60)
        if (currentTime.hour == nextReminderHour and currentTime.minute == nextReminderMinute):
            await bot.send_message(bot.get_channel(nextReminderChannel), nextReminderMessage)
            await asyncio.sleep(60)
        await asyncio.sleep(2)
       
renames = Thread(target = bot.loop.create_task(background_shit()))
#discord = Thread(target = bot.run('MjgzMzEwNjgyNDQ1ODQwMzg0.DDHJ_A.ItxZRmxa_VenCuenguhmG4d-Npw'))

while True:
    try:
        bot.loop.run_until_complete(bot.start('MjgzMzEwNjgyNDQ1ODQwMzg0.DDHJ_A.ItxZRmxa_VenCuenguhmG4d-Npw'))
    except BaseException:
        sleep(5)