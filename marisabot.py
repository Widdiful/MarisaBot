import discord, random, asyncio, os, datetime, re, operator # required
import twitter # twitter api
import ftputil # ftp connection
import requests # addemote
import urllib # gdq
import codecs # archive
from discord.ext import commands # required
from threading import Thread # required
from time import sleep # !startgame
from collections import Counter # chaninfo
from collections import OrderedDict # chanranking
from bs4 import BeautifulSoup # twthread

########################################
#     THIS BEAUTIFUL BOT IS BY WID     #
#               IT'S COOL              #
########################################

########################################
# Some features in this bot are legacy
# and/or have been made very quickly
# and messily. Some that require files
# may need adjustment to work properly.
########################################

########################################
# INITIAL BOT SETUP
# have a botinfo.txt file in the root
# directory with the following information
#
# line 1: twitter api consumer key
# line 2: twitter api consumer secret key
# line 3: twitter api access token key
# line 4: twitter api access token secret key
# line 5: ip address of ftp server
# line 6: username for ftp server
# line 7: password for ftp server
# line 8: discord api key
#
# to disable commands, simply delete the
# function or comment them out. you can
# also feel free to just take these
# commands for your own bot. just don't
# take credit for them.
########################################

# INITIAL BOT SETUP
description = '''I'm Marisa Kirisame! An ordinary magician!'''
bot = commands.Bot(command_prefix='!', description=description)

# login to twitter and ftp
info = open('botinfo.txt').readlines()
for line in info:
    line = line.replace("\r", "").replace("\n", "")

api = twitter.Api(consumer_key=info[0].replace("\n", ""),
                  consumer_secret=info[1].replace("\n", ""),
                  access_token_key=info[2].replace("\n", ""),
                  access_token_secret=info[3].replace("\n", ""))
                  
ipadr = info[4].replace("\n", "")
user = info[5].replace("\n", "")
passw = info[6].replace("\n", "")
ftp = ftputil.FTPHost(ipadr, user, passw)

async def updateEmotes():
    print("attempted to update emotes.")
    # function to replicate local emotes to a server
    ftp = ftputil.FTPHost(ipadr, user, passw)
    files = ftp.listdir('/emotes')
    emotes = os.listdir('emotes')
    for filename in os.listdir('emotes'):
        if filename.replace("?", "`Q") not in files:
            if os.path.isfile('emotes/' + filename):
                print ("uploading " + filename)
                ftp.upload(os.path.join('emotes/', filename), os.path.join('/emotes/', filename.replace("?", "`Q")))
    for filename in files:
        if filename.replace("`Q", "?") not in emotes:
            ftp.remove(os.path.join('/emotes/', filename))
    ftp.close()

async def background_shit():
    # just prints when bot is fully initialised and connected
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
        
        #if (datetime.datetime.now().minute % 10 == 0):
            #await updateEmotes()
        if (currentTime.minute == 0 and currentTime.hour == 0):
            print('butts')
            gennames = open('general.txt').readlines()
            for line in gennames:
                line = line.replace("\r\n", "")
            general = bot.get_channel(123611091086475264)
            newgen = random.choice(gennames)
            while (newgen == general.name and newgen != "general"):
                newgen = random.choice(gennames)
            await general.edit(name = newgen)
            print("changed name to " + newgen)
                
            for server in bot.guilds:
                for srole in server.roles:
                    if srole.id == 340962768582868992:
                        names = open('names.txt').readlines()
                        for line in names:
                            line = line.replace("\r\n", "")
                        await srole.edit(name = random.choice(names))
            await asyncio.sleep(60)
        if (currentTime.hour == nextReminderHour and currentTime.minute == nextReminderMinute):
            #await ctx.channel.send(bot.get_channel(nextReminderChannel), nextReminderMessage)
            await asyncio.sleep(60)
        await asyncio.sleep(2)
    
####################
# COMMANDS
####################

@bot.command()
async def worst(ctx):
    """find out who the worst 2hu is"""
    worsthu = []
    for line in open('text/touhous.txt').readlines():
        worsthu.append(line.replace("\n", ""))
    
    result = random.choice(worsthu)
    if 'Tan Cirno' in result:
        await ctx.send(result + " is the worstanst Touhou")
    elif 'Cirno' in result:
        await ctx.send(result + " is the worstest Touhou")
    elif 'Ringo' in result:
        await ctx.send(result + " is the worst Touhou and Beatle")
    else:
        await ctx.send(result + " is the worst Touhou")

@bot.command()
async def horror(ctx):
    """return something horrible"""
    fpath = os.path.join('/home/pi/marisabot/', 'horror.txt')
    content = random.choice(open(fpath).readlines())
    content1 = content.replace("#", "")
    content2 = content1.replace("\r\n", "")
    await ctx.send('<' + content2 + '>')
        
@bot.command()
async def best(ctx):
    """who is it??"""
    await ctx.send('Marisa Kirisame is the best Touhou')
    
@bot.command()
async def waifu(*args):
    """return a random waifu.txt post"""
    text = ''
    for ar in args:
        text = str(text + ar + ' ')
    while text.endswith(' '):
        text = text[:-1]
    fpath = os.path.join('/home/pi/marisabot/', 'waifu.txt')
    if text == '':
        content = random.choice(open(fpath).readlines())
        content1 = content.replace("#", "")
        content2 = content1.replace("\r\n", "")
        await ctx.send(content2)
    else:
        results = []
        search = open(fpath, 'r')
        for line in search:
            if text.lower() in line.lower():
                results.append(line)
        search.close()
        if len(results) == 0:
            await ctx.send('No results found :(')
        else:
            content = random.choice(results)
            content1 = content.replace("#", "")
            content2 = content1.replace("\r\n", "")
            await ctx.send(content2 + " (" + str(len(results)) + " results)")
            
@bot.command()
async def touhou(*args):
    """return a random 2hu.txt post"""
    text = ''
    for ar in args:
        text = str(text + ar + ' ')
    while text.endswith(' '):
        text = text[:-1]
    fpath = os.path.join('/home/pi/marisabot/', 'touhou.txt')
    if text == '':
        content = random.choice(open(fpath).readlines())
        content = content.replace("\r\n", "")
        content = content.split('//')
        for x in content:
            await ctx.send(x)
    else:
        results = []
        search = open(fpath, 'r')
        for line in search:
            if text.lower() in line.lower(): results.append(line)
        search.close()
        if len(results) == 0:
            await ctx.send('No results found :(')
        else:
            content = random.choice(results)
            content1 = content.replace("\r\n", "")
            content2 = content1.replace('//', "\n")
            await ctx.send(content2 + " (" + str(len(results)) + " results)")

@bot.command()
async def jojo(ctx):
    """jojo memes are shit dont use this"""
    jojowns = []
    for line in open('text/jojo.txt').readlines():
        jojowns.append(line.replace("\n", ""))
    
    await ctx.send(random.choice(jojowns))

@bot.command()
async def fish(ctx):
    """who is the best oc fish"""
    fishList = ['Dottie', 'Greenbird', 'Hamburger', 'Mammoth', 'Mimosa', 'Ol\' Blue', 'Sir Squirt', 'Tang', 'Th\'Lump']
    
    await ctx.send(random.choice(fishList) + " is the best fish")
    
@bot.command()
async def when(ctx):
    """well???"""
    nowh = datetime.datetime.now().strftime("%H")
    nowm = datetime.datetime.now().strftime("%M")
    time = 1260
    diff = time - (int(float(str(nowh) + "." + str(str(int(nowm) / 60).replace("0.", "")))*60))
    result = str(diff)
    if result.startswith("-"):
        result = result.replace("-", "")
        await ctx.send('FishCenter Live started ' + result + ' minutes ago.')
    else:
        await ctx.send('FishCenter Live starts in ' + result + ' minutes.')
        
@bot.command()
async def fit(ctx):
    """💪"""
    await ctx.send('Do ' + str(random.randint(1,100)) + ' reps!')
    
@bot.command()
async def numbers(ctx):
    """return some numbers"""
    text = ctx.message.content.replace('!numbers ', '', 1)
    while text.endswith(' '):
        text = text[:-1]
    big = [25, 50, 75, 100]
    sml = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
    if len(text) > 1 and text[:2].isdigit() == True:
        if int(text[:1]) + int(text[:2][1:]) == 6:
            bigs = int(text[:1])
            smls = int(text[:2][1:])
            bign = []
            smln = []
            if bigs > 0:
                for x in range(0, bigs):
                    result = random.choice(big)
                    bign.append(result)
                    big.remove(result)
            if smls > 0 :
               for x in range(0, smls):
                    result = random.choice(sml)
                    smln.append(result)
                    sml.remove(result)
            await ctx.send(str(bign).replace('[', '').replace(']', '') + ', ' + str(smln).replace('[', '').replace(']', '') + ' to make ' + str(random.randint(0, 999)))
        else:
            await ctx.send('Please only choose six numbers')
    else:
        await ctx.send('Please use !numbers[big][small], for example: !numbers 15')
        
@bot.command()
async def letters(ctx):
    """return some letters"""
    text = ctx.message.content.replace('!letters ', '', 1)
    while text.endswith(' '):
        text = text[:-1]
    vwl = ['a', 'e', 'i', 'o', 'u']
    cns = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    if len(text) > 1 and text[:2].isdigit() == True:
        if int(text[:1]) + int(text[:2][1:]) == 9:
            vwls = int(text[:1])
            cnss = int(text[:2][1:])
            qiz = []
            if vwls > 0:
                for x in range(0, vwls):
                    result = random.choice(vwl)
                    qiz.append(result)
            if cnss > 0:
                for x in range(0, cnss):
                    result = random.choice(cns)
                    qiz.append(result)
            random.shuffle(qiz)
            await ctx.send(str(qiz).replace('[', '').replace(']', '').replace(', ', ' ').replace("'", "").upper())
        else:
            await ctx.send('Please only choose nine letters')
    else:
        await ctx.send('Please use !letters[vowels][consonants], for example: !letters 36')
        
@bot.command()
async def stats(ctx):
    """launcher stats"""
    fpath = os.path.join('/home/pi/marisabot/', 'cumstat.txt')
    stat = open(fpath).readlines()
    for st in stat:
        st = st.replace("\r\n", "")
    await ctx.send('Biscuits came on: ' + stat[0] + '\nBots fought: ' + stat[1] + '\nMans Hanged: ' + stat[4] + '\nlols had: ' + stat[2] + "\nTimes Wid's mum has been mentioned: " + stat[3])
    
@bot.command()
async def tier(ctx):
    """how good is a thing"""
    text = ctx.message.content.replace('!tier', '', 1)
    while text.endswith(' '):
        text = text[:-1]
    worsthu = []
    for line in open('text/touhous.txt').readlines():
        worsthu.append(line.replace("\n", ""))
    tiers = []
    for line in open('text/tiers.txt').readlines():
        tiers.append(line.replace("\n", ""))
    if text == '':
        await ctx.send(random.choice(worsthu).lower() + ' is ' + random.choice(tiers).lower() + ' tier')
    else:
        await ctx.send(text + ' is ' + random.choice(tiers).lower() + ' tier')

@bot.command()
async def points(ctx):
    """all the lads, ranked..."""
    fpath = os.path.join('/home/pi/marisabot/', 'biscuitpoints.txt')
    bp = open(fpath).readlines()
    for line in bp:
        line = line.replace("\r\n", "")
    x = bp[::2]
    y = []
    for line in bp[1::2]:
        y.append(int(line))
    ys, xs = zip(*sorted(zip(y, x), reverse=True))
    await ctx.send("1st: " + str(xs[0]) + " (" + str(ys[0]) + " BP)")
    await ctx.send("2nd: " + str(xs[1]) + " (" + str(ys[1]) + " BP)")
    await ctx.send("3rd: " + str(xs[2]) + " (" + str(ys[2]) + " BP)")
    
@bot.command()
async def totals(ctx):
    """all the lads, ranked... but different"""
    fpath = os.path.join('/home/pi/marisabot/', 'bp_total.txt')
    bp = open(fpath).readlines()
    for line in bp:
        line = line.replace("\r\n", "")
    x = bp[::2]
    y = []
    for line in bp[1::2]:
        y.append(int(line))
    ys, xs = zip(*sorted(zip(y, x), reverse=True))
    await ctx.send("1st: " + str(xs[0]) + " (" + str(ys[0]) + " BP)")
    await ctx.send("2nd: " + str(xs[1]) + " (" + str(ys[1]) + " BP)")
    await ctx.send("3rd: " + str(xs[2]) + " (" + str(ys[2]) + " BP)")
    
@bot.command(pass_context=True)
async def tweet(ctx):
    """post to twitter"""
    text = ctx.message.content.replace('!tweet ', '', 1)
    while text.endswith(' '):
        text = text[:-1]
    global tweeted
    twtmsg = text.split()
    img = ''
    count = 0
    while count < len(twtmsg):
        if str(twtmsg[count]).startswith('http'):
            if '.jpg' in str(twtmsg[count]) or '.png' in str(twtmsg[count]) or '.gif' in str(twtmsg[count]):
                img = twtmsg[count]
                twtmsg.remove(twtmsg[count])
        count = count + 1
    if len(text) <= 140:
        tweet = str(' '.join(twtmsg))
        if img != '':
            tweeted = api.PostMedia(tweet, img)
        else:
            tweeted = api.PostUpdate(tweet)
        await ctx.send('yoink! http://www.twitter.com/REALMarisaBot/status/' + str(tweeted.id) + ' ;)')
    if len(text) > 140:
        twtlen = random.randint(1, 140)
        twtstart = random.randint(0, len(twtmsg))
        twtmsg = twtmsg[twtstart:]
        tweet = str(' '.join(twtmsg))
        if img != '':
            tweeted = api.PostMedia(tweet[:twtlen], img)
        else:
            tweeted = api.PostUpdate(tweet[:twtlen])
        await ctx.send('yoink! http://www.twitter.com/REALMarisaBot/status/' + str(tweeted.id) + ' ;)')
        
@bot.command()
async def delete(ctx):
    """banish from twitter"""
    global tweeted
    deleted = tweeted.id
    api.DestroyStatus(deleted)
    await ctx.send('deleted tweet!')
    
@bot.command()
async def gdq(ctx):
    """gdq shit"""
    text = ctx.message.content.replace('!gdq ', '!gdq', 1).replace('!gdq', '', 1)
    while text.endswith(' '):
        text = text[:-1]
        
    gameList = [None]
    runnerList = [None]
    categoryList = [None]
    timeList = [None]
    gameList.pop(0)
    runnerList.pop(0)
    categoryList.pop(0)
    timeList.pop(0)
    
    req = urllib.request.Request('https://gamesdonequick.com/schedule', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req)
    data = resp.readlines()
    for i in range(0, len(data)):
        line = data[i].decode("utf-8").rstrip()
        if line.startswith('<td class="start-time text-right">'):
            gameList.append(data[i+1].decode("utf-8").rstrip().replace('<td>','').replace('</td>','').replace('&#039;', "'"))
            runnerList.append(data[i+2].decode("utf-8").rstrip().replace('<td>','').replace('</td>','').replace('&#039;', "'"))
            categoryList.append(data[i+7].decode("utf-8").rstrip().replace('<td>','').split(' &mdash')[0].replace('&#039;', "'"))
            timeList.append(data[i+6].decode("utf-8").rstrip().replace('<td class="text-right "> <i class="fa fa-clock-o" aria-hidden="true"></i> ', '').replace(' </td>',''))
            
    gameStrings = [None]
    gameStrings.pop(0)
    for i in range(0, len(gameList)):
        gameStrings.append(gameList[i] + ' (' + categoryList[i] + ') - ' + runnerList[i] + ' (ETA: ' + timeList[i] + ')')
        
    result = ''
    count = 5
    if ('count' in text.lower()):
        count = int(text.lower().split('count:')[1].split()[0])
        text = text.split('count:')[0]
    countAdjust = int(count / 2.0)
    if (countAdjust % 2 == 1):
        countAdjust -= 1
    if text == '':
        url = 'http://widdiful.co.uk/gdqjson.php'
        resp = urllib.request.urlopen(url)
        data = resp.readlines()
        gameName = str(data[6])[:-12][2:]
        
        if len(gameName) > 0:        
            gameFound = False
            for i in range(0, len(gameStrings)):
                if str(gameName).lower() in gameStrings[i].lower() and gameFound == False:
                    for j in range(0, count):
                        if len(gameStrings) > i + j:
                            result = result + str(j) + ': ' + str(gameStrings[i + j]) + '\n'
                    gameFound = True
            if gameFound == False:
                result += ('Now: ' + str(gameName) + '\n')
        else:
            result += "Twitch sucks and I can't find the game."
    elif text.startswith('-'):
        gameTitle = text.replace('-','')
        gameFound = False
        for i in range(0, len(gameStrings)):
            if gameTitle.lower() in gameStrings[i].lower() and gameFound == False:
                for j in range(0 - countAdjust, count - countAdjust):
                    if (j == 0):
                        result += "**"
                    result += (str(-j) + ': ' + str(gameStrings[i - j]) + '\n')
                    if (j == 0):
                        result += "**"
                gameFound = True
        if gameFound == False:
            await ctx.send('No results for "' + gameTitle + '"')
    else:
        gameTitle = text
        gameFound = False
        for i in range(0, len(gameStrings)):
            if gameTitle.lower() in gameStrings[i].lower() and gameFound == False:
                for j in range(0 - countAdjust, count - countAdjust):
                    if len(gameStrings) > i + j:
                        if (j == 0):
                            result += "**"
                        result += (str(j) + ': ' + str(gameStrings[i + j]) + '\n')
                        if (j == 0):
                            result += "**"
                gameFound = True
        if gameFound == False:
            await ctx.send('No results for "' + gameTitle + '"')
    
    await ctx.send(result)

@bot.command()
async def rpg(ctx):
    """generate an rpg character"""
    fpath = os.path.join('/home/pi/marisabot/', 'prefix.txt')
    prefix = open(fpath).readlines()
    for line in prefix:
        line = line.replace("\r\n", "")
    fpath = os.path.join('/home/pi/marisabot/', 'suffix.txt')
    suffix = open(fpath).readlines()
    for line in suffix:
        line = line.replace("\r\n", "")
    fpath = os.path.join('/home/pi/marisabot/', 'wildcard.txt')
    wildcard = open(fpath).readlines()
    for line in wildcard:
        line = line.replace("\r\n", "")
    fpath = os.path.join('/home/pi/marisabot/', 'hissatsu.txt')
    hissatsu = open(fpath).readlines()
    for line in hissatsu:
        line = line.replace("\r\n", "")

    sufA = random.choice(suffix)
    sufB = sufA
    if (random.randint(0,2) == 0):
        sufB = random.choice(suffix)
    preA = random.choice(prefix)
    preB = random.choice(prefix)
    titl = ""
    while preB == preA:
        preB = random.choice(prefix)
    if (preA == 'q' and not sufA.startswith('u')):
        preA += 'u'
    if (preB == 'q' and not sufA.startswith('u')):
        preB += 'u'
    nameA = ''.join([preA, sufA]).replace('\n','')
    if (random.randint(0,1) == 0):
        nameA = random.choice(wildcard)
    nameB = ''.join([preB, sufB]).replace('\n','')
    if (random.randint(0,3) == 0):
        titl = " the " + random.choice(wildcard)
    name = str(nameA + ' ' + nameB + titl).replace('\n','')
        
    result = ' | name: ' + name + ' | class: ' + (random.choice(prefix) + '' + random.choice(suffix)).replace('\n','') + ' | health: ' + random.choice(wildcard) + ' | attack: ' + random.choice(wildcard) + ' | defence: ' + random.choice(wildcard) + ' | agility: ' + random.choice(wildcard) + ' | magic: ' + random.choice(wildcard) + ' | finishing move: ' + nameB + ' ' + random.choice(hissatsu)
    await ctx.send(result.replace('\n','').replace(' |', '\n|'))
    
@bot.command()
async def restart(ctx):
    """restart biscuit game"""
    global p
    global pt
    global winner
    global scores
    global victorymsg
    p = []
    pt = []
    scores = []
    winner = ""
    await ctx.send('Game restarted!')
    
@bot.command(pass_context=True)
async def joingame(ctx):
    """join the biscuit game"""
    joinmsg = []
    for line in open('text/joinmsg.txt').readlines():
        joinmsg.append(line.replace("\n", ""))

    global p
    global pt
    global scores
    global winner
    newplayer = ""
    nick = ctx.message.author.name
    try:
        p
    except NameError:
        p = []
        pt = []
        scores = []
        winner= ""
    if not len(p) >=15:
        if not nick in p:
            p.append(nick)
            newplayer = nick
            newscore = random.randint(1, 15)
            while newscore in pt:
                newscore = random.randint(1, 15)
            pt.append(newscore)
            await ctx.send(newplayer + " " + random.choice(joinmsg))
            for x in p:
                high = pt.index(max(pt, key=float))
                winner = p[high]
        else:
            await ctx.send('You\'re already in the game, chucklefuck')
    else:
        await ctx.send('Game full!')

@bot.command()
async def players(ctx):
    """who in"""
    global p
    global pt
    global scores
    players = []
    global victorymsg
    try:
        p
    except NameError:
        p = []
        pt = []
        scores = []
        winner= ""
    if p == []:
        await ctx.send('Game empty!')
    else:
        playerlist = str(sorted(p, key=str.lower))
        playerlist1 = playerlist.replace("[", "")
        playerlist2 = playerlist1.replace("]", "")
        playerlist3 = playerlist2.replace("'", "")
        await ctx.send('Current players: ' + playerlist3 + ' (' + str(len(p)) + '/15)')
        
@bot.command()
async def startgame(ctx):
    """initiate biscuits"""
    global p
    global pt
    global winner
    global scores
    global victorymsg
    victorymsgexists = True
    losemsg = []
    for line in open('text/losemsg.txt').readlines():
        losemsg.append(line.replace("\n", ""))
        
    try:
        cumjar
    except NameError:
        cumjarPopulated = False
    if cumjarPopulated == True:
        if len(cumjar) == 0:
            cumjarPopulated = False
    if cumjarPopulated == False:
        fpath = os.path.join('/home/pi/marisabot/', 'cumjar.txt')
        cumjar = open(fpath).readlines()
        for line in cumjar:
            line = line.replace("\r\n", "")
    if p == []:
        await ctx.send('Join the game first you enormous idiot')
    if len(p) == 1:
        await ctx.send('You can\'t play soggy biscuit by yourself! It\'s either a cum biscuit or no biscuit at all, I\'m afraid.')
    elif winner != "":
        ptsort, psort = zip(*sorted(zip(pt,p)))
        point_getter = psort[0].replace("_","")
        points = len(p) - 1
        for y in range(0, sorted(pt, key=float)[-1]):
            for x in range(0, len(sorted(pt, key=float))):
                if y == ptsort[x]:
                    await ctx.send(psort[x] + ' ' + random.choice(losemsg))
                    if not psort[x] == point_getter:
                        points = points - 1
            sleep(1)
        prize = random.choice(cumjar)
        await ctx.send(winner + ' is the winner! Bon appetit! Here\'s your prize! ' + prize)
        cumjar.remove(prize)
        p = []
        pt = []
        scores = []
        winner = ""
            
@bot.command()
async def coin(ctx):
    """its what you think !flip should do"""
    if random.randrange(0, 2):
        await ctx.send('heads')
    else:
        await ctx.send('tails')
        
@bot.command()
async def flip(ctx):
    """its !coin"""
    if random.randrange(0, 2):
        await ctx.send('heads')
    else:
        await ctx.send('tails')
        
@bot.command(pass_context = True)
async def roll(ctx):
    """roll the dice"""
    text = ctx.message.content
    results = []
    maths = []
    for i in range(len(text.split(' '))):
        rolls = []
        input = text.split(' ')[i]
        if input[0].isdigit():
            input = re.split('(\d+|\D+)',input)
            input = list(filter(None, input))
            if len(input) >= 2:
                diceNo = int(input[0])
                sideNo = int(input[2])
            for j in range(diceNo):
                rolls.append(random.randrange(1, sideNo + 1))
            if len(input) >= 4:
                for j in range(0, len(input) - 4, 2):
                    type = input[j + 3]
                    typeNo = int(input[j + 4])
                    
                    if type == 'd':
                        for k in range(typeNo):
                            rolls.remove(min(rolls))
                    if type == 'dh':
                        for k in range(typeNo):
                            rolls.remove(max(rolls))
                    elif type == 'k':
                        for k in range(len(rolls) - typeNo):
                            rolls.remove(min(rolls))
                    elif type == 'kl':
                        for k in range(len(rolls) - typeNo):
                            rolls.remove(max(rolls))
                    elif type == '+':
                        rolls.append(typeNo)
                    elif type == '-':
                        rolls.append(typeNo * -1)
            rolls = [ int(x) for x in rolls ]
            await ctx.send(ctx.message.author.display_name + ': ' + str(rolls) + ' = ' + str(sum(rolls)))
            results.append(sum(rolls))
        else:
            if input[0] == '+' or input[0] == '-':
                maths.append(input[0])
    if len(maths) > 0:
        mathsStr = str(results[0])
        endResult = results[0]
        for i in range(len(maths)):
            if maths[i] == '+':
                endResult += results[i + 1]
                mathsStr += " + " + str(results[i + 1])
            elif maths[i] == '-':
                endResult -= results[i + 1]
                mathsStr += " - " + str(results[i + 1])
        mathsStr += " = " + str(endResult)
        await ctx.send(mathsStr)
            
@bot.command(pass_context = True)
async def ball(ctx):
    """ask marisa a personal question"""
    _responses = {'positive': ['It is possible.', 'Yes!', 'Of course.',
                               'Naturally.', 'Obviously.', 'It shall be.',
                               'The outlook is good.', 'It is so.',
                               'One would be wise to think so.',
                               'The answer is certainly yes.'],
                  'negative': ['In your dreams.', 'I doubt it very much.',
                               'No chance.', 'The outlook is poor.',
                               'Unlikely.', 'About as likely as pigs flying.',
                               'You\'re kidding, right?', 'NO!', 'NO.', 'No.',
                               'The answer is a resounding no.', ],
                  'unknown' : ['Maybe...', 'No clue.', '_I_ don\'t know.',
                               'The outlook is hazy, please ask again later.',
                               'What are you asking me for?', 'Come again?',
                               'You know the answer better than I.',
                               'The answer is def-- oooh! shiny thing!'],
                 }
    if len(ctx.message.content) % 3 == 0:
        category = 'positive'
    elif len(ctx.message.content) % 3 == 1:
        category = 'negative'
    else:
        category = 'unknown'
    await ctx.send(random.choice(_responses[category]))
    
@bot.command(pass_context = True)
async def poll(ctx):
    """create a poll"""
    letter = ['1⃣', '2⃣','3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟',  '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']
    if len(ctx.message.content.split(' ')) > 1:
        count = ctx.message.content.split(' ')[1]
        if count.isdigit():
            toCount = int(count)
            if toCount > 20:
                remainder = toCount - 20
                toReact = 20
                for i in range(toReact):
                    await ctx.message.add_reaction(letter[i])
                continued = await ctx.channel.send("...")
                for i in range(remainder):
                    if (i + 20) < len(letter):
                        await continued.add_reaction(letter[i + 20])
                if toCount > 36:
                    await ctx.send("fucking hell how many options do you need")
                    await continued.add_reaction('🖕')
            else:
                for i in range(toCount):
                    await ctx.message.add_reaction(letter[i])
        else:
            toCount = ctx.message.content.count(', ') + ctx.message.content.count(' or ') - ctx.message.content.count(', or ') + 1
            if toCount > 1:
                for i in range(toCount):
                    await ctx.message.add_reaction(letter[i])
            else:
                await ctx.message.add_reaction('👍')
                await ctx.message.add_reaction('👎')
    else:
        await ctx.send("what are you polling for, dumbass")
    
@bot.command(pass_context = True)
async def nickme(ctx):
    """one nickname please"""
    nicktype = random.randint(0,1)
    if nicktype == 0:
        prefix = ['b', 'c', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'ph', 'q', 'r', 'rh', 's', 'sn', 'st', 't', 'th', 'v', 'w', 'wh', 'wr', 'y', 'z']
        suffix = ['umbus', 'ungus', 'ungis', 'ungo', 'umbo', 'uggle', 'uddle', 'ubble', 'uggus', 'umpus', 'imbus', 'ingus', 'ingo', 'imbo', 'iggle', 'iddle', 'ibble', 'iggus', 'impus', 'izzo', 'ombus', 'ongus', 'ongo', 'ombo', 'oggle', 'oddle', 'obble', 'oggus', 'orgis', 'ompus', 'eenis']
        wildcard = ['mystic', 'final', 'ultimate', 'beautiful', 'cursed', 'blessed', 'powerful', 'eternal', 'magical', 'all-knowing', 'sacred', 'holy', 'supreme', 'legendary', 'wonderful', 'terrific', 'genius', 'hallowed', 'thicc', 'extra', 'great', 'baffling', 'haunted', 'incredible', 'spooky', 'good', 'bad', 'fuzzy', 'speedy', 'nifty', 'swell', 'fast', 'slow', 'spiffy', 'awful', 'smelly', 'punished', 'damaged', 'tired', 'sleepy', 'lit', 'wise', 'brave', 'mad']
        sufA = random.choice(suffix)
        sufB = sufA
        if (random.randint(0,2) == 0):
            sufB = random.choice(suffix)
        preA = random.choice(prefix)
        preB = random.choice(prefix)
        titl = ""
        while preB == preA:
            preB = random.choice(prefix)
        if (preA == 'q' and not sufA.startswith('u')):
            preA += 'u'
        if (preB == 'q' and not sufA.startswith('u')):
            preB += 'u'
        nameA = preA + sufA
        if (random.randint(0,1) == 0):
            nameA = random.choice(wildcard)
        nameB = preB + sufB
        newnick = nameA + ' ' + nameB
        if (random.randint(0,1) == 0):
            newnick = newnick + ' the ' + random.choice(wildcard)
    elif nicktype == 1:
        polnames = ['edgy', 'fuck', 'cum', 'shit', 'balls', 'fart', 'fedora', 'lord', 'man', 'boy', 'nut', 'pants', 'weeb', 'loser', 'cummy', 'piss', 'ass']
        nametype = random.randint(0,3)
        if (nametype == 0):
            newnick = random.choice(polnames) + ' ' + random.choice(polnames) + random.choice(polnames)
        if (nametype == 1):
            newnick = random.choice(polnames) + random.choice(polnames) + ' ' + random.choice(polnames)
        if (nametype == 2):
            newnick = random.choice(polnames) + random.choice(polnames) + ' ' + random.choice(polnames) + random.choice(polnames)
        if (nametype == 3):
            newnick = random.choice(polnames) + ' ' + random.choice(polnames)
    await ctx.send("i now declare you {}".format(newnick))
    await bot.change_nickname(ctx.message.author, newnick)

@bot.command(pass_context = True)
async def emote(ctx):
    """post an emote"""
    if len(ctx.message.content.replace("!emote","")) > 0:
        emote = ctx.message.content.replace("!emote","").split()[0].replace("?", "_")
        toPost = ctx.message.content.replace("!emote " + emote, "", 1)
        for filename in os.listdir('emotes'):
            if '.' in filename and filename.replace("~.",".").split('.')[0].lower() == emote.lower():
                with open('emotes/' + filename, 'rb') as f:
                    await ctx.channel.trigger_typing()
                    await ctx.channel.send(content="**" + ctx.message.author.display_name + "**:" + toPost, file=discord.File(f))
                    await ctx.message.delete()
    else:
        await ctx.send("List of emotes: http://widdiful.co.uk/marisabot/emotes.php")
        
@bot.command(pass_context = True)
async def randemote(ctx):
    """post a mystery emote"""
    if len(ctx.message.content.replace("!randemote","")) > 0:
        emote = ctx.message.content.replace("!randemote","").split()[0]
        toPost = ctx.message.content.replace("!randemote " + emote, "", 1)
        if os.path.exists('emotes/' + emote):
            image = random.choice(os.listdir('emotes/' + emote))
            await ctx.channel.send(content="(Random) **" + ctx.message.author.display_name + "**:" + toPost, file=discord.File('emotes/' + image))
            await ctx.message.delete()
    else:
        toPost = ctx.message.content.replace("!randemote", "", 1)
        image = random.choice(os.listdir('emotes/'))
        await ctx.channel.send(content="(Random) **" + ctx.message.author.display_name + "**:" + toPost, file=discord.File('emotes/' + image))
        await ctx.message.delete()

@bot.command(pass_context = True)        
async def updateemote(ctx):
    """wid-only spell"""
    if (ctx.message.author.id == "126081812714881025"):
        emotes = os.listdir('emotes')
        await ctx.send("updating emotes...")
        await updateEmotes()
        await ctx.send("updated emotes. current total: " + str(len(emotes)))
    else:
        await ctx.send("you aint wid, fuck off")
        
@bot.command(pass_context = True)
async def addemote(ctx):
    """add an emote"""
    if (len(ctx.message.attachments) > 0):
        if len(ctx.message.content) > 1:
            filename = ctx.message.content.split()[1]
            filename = filename + "." + ctx.message.attachments[0].filename.split('.')[1]
        else:
            filename = ctx.message.attachments[0]["filename"]
        #filename = filename.replace("?", "_")
        fname = os.path.splitext(filename)[0]
        files_no_ext = [".".join(f.split(".")[:-1]) for f in os.listdir("emotes/") if os.path.isfile("emotes/" + f)]
        r = requests.get(ctx.message.attachments[0].url, stream=True)
        #if 340962768582868992 in [y.id for y in ctx.message.author.roles]:

        if True:
            #if os.path.isfile("emotes/" + filename) == False:
            if fname not in files_no_ext:
                with open ("emotes/" + filename, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
                    await ctx.send("image added")
            else:
                with open ("queue/" + filename, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
                    await ctx.send("name already exists, image added to queue")
#        else:
#            with open ("queue/" + filename, 'wb') as f:
#                for chunk in r:
#                    f.write(chunk)
#                await ctx.send("image added to queue")
    else:
        await ctx.send("upload an image idiot")
        
@bot.command()
async def wotif(ctx):
    """well????"""
    techs = open('text/tech.txt').readlines()
    for line in techs:
        line = line.replace("\r\n", "")
    nouns = open('text/noun.txt').readlines()
    for line in nouns:
        line = line.replace("\r\n", "")
    verbs = open('text/verb.txt').readlines()
    for line in verbs:
        line = line.replace("\r\n", "")
    adjs = open('text/adj.txt').readlines()
    for line in adjs:
        line = line.replace("\r\n", "")
    qmark = ['?', '??', '???']
    tech = random.choice(techs)
    if (random.randint(0,1) == 0):
        result = ("wot if " + tech + " " + random.choice(verbs) + " " + random.choice(nouns) + random.choice(qmark)).replace("\n", "")
    else:
        result = ("wot if " + random.choice(nouns) + " " + random.choice(verbs) + " " + tech + random.choice(qmark)).replace("\n", "")
    if (random.randint(0,1) == 0):
        result = (result + " and " + tech + " was " + random.choice(adjs) + random.choice(qmark)).replace("\n", "")
        if (random.randint(0,1) == 0):
            tech2 = random.choice(techs)
            while (tech2 == tech):
                tech2 = random.choice(techs)
            result = (result + " but what was " + tech2 + " ..." + random.choice(qmark)).replace("\n", "")
    await ctx.send(result)

@bot.command(pass_context = True)
async def chaninfo(ctx):
    """returns info about current/given channel"""
    
    # Detect channel and result count
    msg = ctx.message.content.replace("!chaninfo", "")
    specifyChannel = False
    specifyCount = 5
    if len(msg) > 0:
        channelQuery = msg.split()[0]
        for each in ctx.message.guild.channels:
            if each.name == channelQuery:
                specifyChannel = True
                channel = each
        if len(msg.split()) > 1:
            if msg.split()[1].isdigit():
                specifyCount = int(msg.split()[1])
    if not specifyChannel:
        channel = ctx.message.channel
            
    # Start getting information
    createdDate = channel.created_at.strftime('%d/%m/%Y')
    daysSince = (datetime.datetime.now() - channel.created_at).days
    totalPosts = 0
    posters = [None]
    uniquePosters = 0
    posters.pop(0)
    
    # Find posts in last week
    async for x in channel.history(limit=10000000, after=(datetime.datetime.now() - datetime.timedelta(days=7))):
        totalPosts += 1
        if not x.author.name in posters:
            uniquePosters = uniquePosters + 1
        posters.append(x.author.name)
        
    # Calculations
    if (specifyCount > uniquePosters):
        specifyCount = uniquePosters
    perDay = totalPosts / 7
    posterString = ''
    if len(posters) > 0 and totalPosts > 0:
        posterDict = Counter(posters)
        posters = sorted(posterDict.items(), key=operator.itemgetter(1), reverse = True)
        posterNames = [(k, posterDict[k]) for k in sorted(posterDict, key=posterDict.get, reverse = True)]
        posterString += '\n\n**Top posters:**'

        offset = 0
        i = 0
        while i < specifyCount + offset:
            if len(posterNames) > i:
                try:
                    posterString += '\n**#' + str(i + 1 - offset) + ':** ' + posterNames[i][0] + ' (' + str(posterNames[i][1]) + ')'
                    i += 1
                except:
                    i += 1
                    offset += 1
                    i = (specifyCount + offset) * 10
                    pass
            
    await ctx.send('**' + channel.name.capitalize() + '**\n**Date created:** ' + createdDate + '\n**Days since creation:** ' + str(daysSince) + '\n**Total posts in last 7 days:** ' + str(totalPosts) + '\n**Posts per day:** ' + str(perDay) + posterString)

@bot.command(pass_context = True)
async def userinfo(ctx):
    """returns some info on poster"""
    user = ctx.message.author
    await ctx.send(user.joined_at)
    
@bot.command(pass_context = True)
async def randpost(ctx):
    """get a random post from you in the last week"""
    posts = [None] * 2
    attach = [None] * 2
    msg = ""
    async for x in bot.logs_from(ctx.message.channel, limit=10000000, after=(datetime.datetime.now() - datetime.timedelta(days=7))):
        if x.author.id == ctx.message.author.id:
            posts.append(x.content)
            if len(x.attachments) > 0:
                attach.append(x.attachments[0])
            else:
                attach.append(None)
    rand = random.randint(0, len(posts))
    msg = posts[rand]
    img = attach[rand]
    if img:
        await ctx.send('**' + ctx.message.author.display_name + ':** ' + msg + '\n' + img["url"])
    else:
        await ctx.send('**' + ctx.message.author.display_name + ':** ' + msg)
  
@bot.command(pass_context = True)
async def suikatest(ctx):
    server = ctx.message.guild
    suika = server.get_member('278396115634880522')
    await ctx.send('hi suika')
    msg = await ctx.send('!balls ' + str(ctx.message.channel.id) + ' discord is shit')
    await ctx.message.delete(msg)
    
@bot.command(pass_context = True)
async def twimg(ctx):
    """post all images in a tweet"""
    for i in ctx.message.content.split():
        if 'http' in i and 'twitter.com/' in i:
            id = i.split('/')[-1]
            if '?' in id:
                id = id.split('?')[0]
            tweet = api.GetStatus(id)
            if tweet:
                if tweet.media:
                    if len(tweet.media) > 1:
                        for i in range(1, len(tweet.media)):
                            await ctx.send(tweet.media[i].media_url)
                else:
                    await ctx.send("sorry, twitter api is bad")
    if not 'twitter.com/' in ctx.message.content:
        await ctx.send('post a tweet idiot')
        
@bot.command(pass_context = True)
async def twthread(ctx):
    url = ''
    for i in ctx.message.content.split():
        if 'http' in i and 'twitter.com/' in i:
            url = i
            break
    
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    thread = soup.find('li', {"class": "ThreadedConversation ThreadedConversation--selfThread"})
    posts = thread.find_all('p')
    reply = ''
    for p in posts:
        reply = reply + '\n\n' + str(p.text)
    await ctx.send(reply)
    
@bot.command(pass_context = True)
async def op(ctx):
    image = random.choice(os.listdir('op/'))
    toPost = ctx.message.content.replace("!op", "", 1)
    await ctx.message.delete()
    await ctx.channel.trigger_typing()
    await ctx.channel.send(content="**" + ctx.message.author.display_name + "**:" + toPost, file=discord.File('op/' + image))

@bot.command(pass_context = True)
async def remindme(ctx):
    reminders = []
    for line in open('text/reminders.txt').readlines():
        reminders.append(line.replace("\n", ""))
    message = ctx.message.content.split(' ', 1)[1]
    reminderHour = message.split(':')[0]
    reminderMinute = message.split()[0].split(':')[1]
    
    if ('+' in reminderMinute):
        hourChange = reminderMinute.split('+')[1]
        reminderMinute = reminderMinute.split('+')[0]
        reminderHour = str(int(reminderHour) - int(hourChange))
    elif('-' in reminderMinute):
        hourChange = reminderMinute.split('-')[1]
        reminderMinute = reminderMinute.split('-')[0]
        reminderHour = str(int(reminderHour) + int(hourChange))
        
    reminderHour = int(reminderHour)
    if (reminderHour < 0):
        reminderHour += 24
    elif (reminderHour > 24):
        reminderHour -= 24
    reminderHour = str(reminderHour)
    
    reminderChannel = ctx.message.channel.id
    reminderUser = ctx.message.author.id
    reminderMessage = message.split(' ', 1)[1]
    
    newReminder = (reminderHour + ':' + reminderMinute + ' ' + reminderChannel + ' <@' + reminderUser + '> ' + reminderMessage)
    await ctx.send(newReminder)
    
@bot.command(pass_context = True)
async def moneyness(ctx):
    query = ctx.message.content.split(" ", 1)[1]
    state = random.getstate()
    random.seed(query.lower())
    await ctx.send(query + " is a " + str(random.randint(0, 30)) + " on the moneyness scale.")
    random.setstate(state)
    
@bot.command(pass_context = True)
async def archive(ctx):
    if (ctx.message.author.id == 126081812714881025):
        await ctx.send("starting archive...")
        messages = []
        async for x in ctx.channel.history(limit=10000000):
            currentMessage = ""
            currentMessage += (x.created_at.strftime("%Y-%m-%d %H:%M:%S") + " " + x.author.name + "\n")
            if len(x.content) > 0:
                currentMessage += (x.content + "\n")
            if len(x.attachments) > 0:
                for attachment in x.attachments:
                    currentMessage += (attachment.url + "\n")
            currentMessage += ("\n")
            messages.append(currentMessage)
            
        f = codecs.open("archives/" + ctx.message.channel.name + ".txt", "w+", "utf-8")
        for x in reversed(messages):
            f.write(x)
        f.close()
        await ctx.send("archive complete")
        await ctx.channel.send(file=discord.File('archives/' + ctx.message.channel.name + '.txt'))
    else:
        await ctx.send("wid use only")
    
@bot.command(pass_context = True)
async def chanrank(ctx):
    """all the channels, ranked"""
                
    # Start getting information
    await ctx.send('this will take a while...')
    
    totalPosts = 0
    channels = {}
    
    # Find posts in last week
    for channel in ctx.message.guild.channels:
        try:
            async for x in channel.history(limit=10000000, after=(datetime.datetime.now() - datetime.timedelta(days=7))):
                totalPosts += 1
                channels[channel.name] = channels.get(channel.name, 0) + 1
        except:
            pass
        
    # Calculations
    perDay = totalPosts / 7
    posterString = ''
    if len(channels) > 0 and totalPosts > 0:
        #orderedChannels = OrderedDict(channels)
        orderedChannels = OrderedDict(sorted(channels.items(), key=operator.itemgetter(1), reverse = True))
        #channels = sorted(channels.items(), key=operator.itemgetter(1), reverse = True)

        keys = list(orderedChannels.keys())
        vals = list(orderedChannels.values())
        for i in range(0, len(channels)):
            posterString += '\n**#' + (str(i + 1)) + ':** ' + str(keys[i]) + ' (' + str(vals[i]) + ')'
            
    await ctx.send('\n**Total posts in last 7 days:** ' + str(totalPosts) + '\n**Posts per day:** ' + str(perDay) + posterString)
    
@bot.command(pass_context = True)
async def userrank(ctx):
    """all the users, ranked"""
                
    # Start getting information
    await ctx.send('this will take a while...')
    
    msg = ctx.message.content.replace("!userrank", "")
    
    specifyCount = 5
    if len(msg) > 0:
        if msg.split()[0].isdigit():
            specifyCount = int(msg.split()[0])
    
    totalPosts = 0
    users = {}
    
    # Find posts in last week
    for channel in ctx.message.guild.channels:
        try:
            async for x in channel.history(limit=10000000, after=(datetime.datetime.now() - datetime.timedelta(days=7))):
                totalPosts += 1
                users[x.author.name] = users.get(x.author.name, 0) + 1
        except:
            pass
        
    # Calculations
    perDay = totalPosts / 7
    posterString = ''
    if len(users) < specifyCount:
        specifyCount = len(users)
    if specifyCount > 0 and totalPosts > 0:
        #orderedChannels = OrderedDict(channels)
        orderedChannels = OrderedDict(sorted(users.items(), key=operator.itemgetter(1), reverse = True))
        #channels = sorted(channels.items(), key=operator.itemgetter(1), reverse = True)

        keys = list(orderedChannels.keys())
        vals = list(orderedChannels.values())
        for i in range(0, specifyCount):
            posterString += '\n**#' + (str(i + 1)) + ':** ' + str(keys[i]) + ' (' + str(vals[i]) + ')'
            
    await ctx.send('\n**Total posts in last 7 days:** ' + str(totalPosts) + '\n**Posts per day:** ' + str(perDay) + posterString)
####################
# RUNS ON EVERY NEW MESSAGE, INCLUDING OWN
####################
    
@bot.event
async def on_message(message):
    global hugs
    try:
        hugs
    except NameError:
        hugs = 0
        
    if (message.author.id != 283310682445840384): # ignore own posts
        now = datetime.datetime.now()
        timestamp = "(%02d/%02d)[%02d:%02d]" % (now.day, now.month, now.hour, now.minute)
        
        # put user IDs (int) in here to make the bot ignore them
        banlist = []
        if not message.author.id in banlist:
        
            # hug chain
            if '🤗' in message.content:
                hugs += 1
                if hugs >= 3:
                    await message.channel.send('🤗')
                    hugs = 0
            else:
                hugs = 0
                
            # log a command
            if message.content.startswith('!'):
                try:
                    print (timestamp + "command '" + message.content + "' from user " + message.author.name)
                except:
                    pass
                
            # lists how many images are in a tweet, if more than 1
            if not message.content.startswith('!twimg'):
                for i in message.content.split():
                    if 'http' in i and 'twitter.com/' in i:
                        id = i.split('/')[-1].split('?')[0]
                        tweet = api.GetStatus(id)
                        if tweet:
                            if tweet.media is not None:
                                if len(tweet.media) > 1:
                                    await message.channel.send('Tweet has ' + str(len(tweet.media)) + ' images.')
                    
            # random tweeting
            if random.randint(0, 128) == 10 and not '@' in message.content and not message.content.startswith('!') and not '||' in message.content:
                if message.channel.id == 123611091086475264:
                    global tweeted
                    twtmsg = message.content.split()
                    img = ''
                    count = 0
                    while count < len(twtmsg):
                        if str(twtmsg[count]).startswith('http'):
                            if '.jpg' in str(twtmsg[count]) or '.png' in str(twtmsg[count]) or '.gif' in str(twtmsg[count]):
                                img = twtmsg[count]
                                twtmsg.remove(twtmsg[count])
                        count = count + 1
                    if len(message.content) <= 140:
                        tweet = str(' '.join(twtmsg))
                        if img != '':
                            tweeted = api.PostMedia(tweet, img)
                        else:
                            tweeted = api.PostUpdate(tweet)
                        await message.channel.send('yoink! http://www.twitter.com/REALMarisaBot/status/' + str(tweeted.id) + ' ;)')
                    if len(message.content) > 140:
                        twtlen = random.randint(1, 140)
                        twtstart = random.randint(0, len(twtmsg))
                        tweet = str(' '.join(twtmsg))
                        if img != '':
                            tweeted = api.PostMedia(tweet[:twtlen], img)
                        else:
                            tweeted = api.PostUpdate(tweet[:twtlen])
                        await message.channel.send('yoink! http://www.twitter.com/REALMarisaBot/status/' + str(tweeted.id) + ' ;)')
                        
            marisatxt = []
            for line in open('text/marisatxt.txt').readlines():
                marisatxt.append(line.replace("\n", ""))
            
            # reply to mentions
            for server in bot.guilds:
                if server.me.mentioned_in(message):
                    await message.channel.send(random.choice(marisatxt).replace('NICKNAME', message.author.name))
                   
            # take action against users who post trigger words
            polnames = ['edgy', 'fuck', 'cum', 'shit', 'balls', 'fart', 'fedora', 'lord', 'man', 'boy', 'nut', 'pants', 'weeb', 'loser', 'cummy', 'piss', 'ass']
            triggers = ['cuck', 'nigger', 'kike'] # im sorry that these have to be written down
            for trig in triggers:
                if trig in message.content.lower():
                    satorin = []
                    for line in open('text/satorin.txt').readlines():
                        satorin.append(line.replace("\n", ""))
                    newnick = random.choice(polnames) + ' ' + random.choice(polnames) + random.choice(polnames)
                    await bot.change_nickname(message.author, newnick)
                    await message.channel.send(random.choice(satorin))
                
            # quick post emotes
            isEmote = False
            if message.content.startswith("!"):
                emote = message.content.replace("!","", 1).split()[0]
                toPost = message.content.replace("!" + emote, "")
                for filename in os.listdir('emotes'):
                    if '.' in filename and filename.replace("~.",".").split('.')[0].lower() == emote.lower():
                        with open('emotes/' + filename, 'rb') as f:
                            try:
                                await message.delete()
                            except:
                                pass
                            await message.channel.trigger_typing()
                            await message.channel.send(content="**" + message.author.display_name + "**:" + toPost, file=discord.File(f))
                            isEmote = True
            if message.content.startswith('!') and message.content.split()[0].endswith('ing') and isEmote == False:
                await message.channel.send(message.content.split()[0].replace('!','').replace('ing', 'ong'))
                
            blockedChannels = [358378637583581194, 560947509464399892] # put any channel IDs in here if you dont want the bot to shitpost in there. commands will still run
            cocoID = 234834826081992704
            if not message.content.startswith("!") and not message.channel.id in blockedChannels:        
                msg = message.content.lower()
                
                # post at random
                postChance = 128
                if 'marisa' in msg:
                    postChance = 32
                
                if random.randint(1,postChance) == 10:
                    if not message.channel.id in blockedChannels:
                        if message.author.id == cocoID:
                            await message.channel.send('hahahaha ANOTHER brilliant post by coco')
                        else:
                            await message.channel.send(random.choice(marisatxt).replace('NICKNAME', message.author.name))

                # respond to lovers
                elif "i love" in msg and "marisa" in msg:
                    await message.channel.send('I love you too!!')
                    
                # respond to sick puns
                elif msg.startswith('more like') or '? more like' in msg or ', more like' in msg:
                    if msg.endswith('!!') and len(msg) >= 13:
                        sickpun = []
                        for line in open('text/sickpun.txt').readlines():
                            sickpun.append(line.replace("\n", ""))
                        await message.channel.send(random.choice(sickpun).replace('NICKNAME', message.author.name))
                        
                # respond to potential dad puns
                if msg.startswith('im ready') or msg.startswith("i'm ready"):
                    if len(msg.split()) == 2:
                        await message.channel.send('hi Ready!, im a lady!') # please play the idolmaster million live theater days
                elif msg.startswith('im lady') or msg.startswith("i'm lady"):
                    if len(msg.split()) == 2:    
                        await message.channel.send('hajimeyou!')
                elif msg.startswith('im ') or msg.startswith("i'm "):
                    if len(msg.split()) == 2:
                        await message.channel.send('hi ' + msg.split()[1] + ', im marisa!')
                elif msg.startswith('i am '):
                    if len(msg.split()) == 3:
                        await message.channel.send('hi ' + msg.split()[2] + ', im marisa!')
                elif msg.startswith('im a ') or msg.startswith("i'm a "):
                    if len(msg.split()) == 3:
                        await message.channel.send('hi ' + msg.split()[2] + ', im marisa!')

            if isEmote == False:
                await bot.process_commands(message) # run commands on this message

            
# RUNS BOTS
renames = Thread(target = bot.loop.create_task(background_shit()))
bot.loop.run_until_complete(bot.start(info[7]))

while True:
    try:
        bot.loop.run_until_complete(bot.connect())
    #except (Exception, ConnectionResetError, ftputil.error.FTPOSError, RuntimeError) as e:
    except RuntimeError:
        bot = commands.Bot(command_prefix='!', description=description)
        print("runtime error")
        sleep(5)
    except:
        print("generic error")
        sleep(5)