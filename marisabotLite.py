import discord, random, asyncio, os, datetime, re, operator # required
import twitter # twitter api
import urllib # gdq
from discord.ext import commands # required
from threading import Thread # required
from time import sleep # required
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
# line 5: discord api key
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
info = open('botinfolite.txt').readlines()
for line in info:
    line = line.replace("\r", "").replace("\n", "")

api = twitter.Api(consumer_key=info[0].replace("\n", ""),
                  consumer_secret=info[1].replace("\n", ""),
                  access_token_key=info[2].replace("\n", ""),
                  access_token_secret=info[3].replace("\n", ""))

async def background_shit():
    # just prints when bot is fully initialised and connected
    await bot.wait_until_ready()
    print ('connected')

####################
# COMMANDS
####################
    
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
    async for x in ctx.message.channel.history(limit=10000000, after=(datetime.datetime.now() - datetime.timedelta(days=7))):
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
                    if 'video' in tweet.media[0].type:
                        await ctx.send(tweet.media[0].video_info['variants'][0]['url'])
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
    
    specifyCount = 20
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
        
    if (message.author.id != 333315409488904192): # ignore own posts
        now = datetime.datetime.now()
        timestamp = "(%02d/%02d)[%02d:%02d]" % (now.day, now.month, now.hour, now.minute)
        
        # put user IDs (int) in here to make the bot ignore them
        banlist = []
        if not message.author.id in banlist:
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
                        id = i.split('/')[-1].split('?')[0].split('>')[0]
                        tweet = api.GetStatus(id)
                        if tweet:
                            if tweet.media is not None:
                                if len(tweet.media) > 1:
                                    await message.channel.send('Tweet has ' + str(len(tweet.media)) + ' images.')
                                if 'video' in tweet.media[0].type:
                                    await message.channel.send(tweet.media[0].video_info['variants'][0]['url'])
            
            await bot.process_commands(message)

# RUNS BOTS
renames = Thread(target = bot.loop.create_task(background_shit()))
bot.loop.run_until_complete(bot.start(info[4]))

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