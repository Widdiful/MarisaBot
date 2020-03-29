require 'discordrb'
require 'cinch'

discord_bot = Discordrb::Commands::CommandBot.new token: '123', client_id: 123
irc_channel = "#touhou-launcher"

irc_bot = Cinch::Bot.new do
  configure do |c|
    c.server = "irc.rizon.net"
    c.channels = [irc_channel]
    c.nick = "MarisaBot_"
  end

  @colours = [:red, :teal, :pink, :purple, :orange, :royal, :blue, :green, :brown]
  on :message, /(.+)/ do |m, text|
	#words = text.split
	#for word in words
	#  word.sub!(/^\:.*\:$/, '`' + word + '`' )
	#  word.sub!(/^\<:.*\>$/, '`' + word + '`' )
	#end
	#text = words.join(" ")
    discord_bot.send_message(123611091086475264, "`<#{m.user.nick}>` #{text}", tts = false, embed = nil)
  end

  discord_bot.message(in: 123611091086475264) do |event, *args1|
    content = event.message.content
    event.message.mentions.each{|user| content = content.gsub("<@" + user.id.to_s + ">", "@" + user.username)}
    if event.message.attachments.empty?
      Channel(irc_channel).send(Format(@colours.sample(random: Random.new(event.user.id.to_i)), "\<" + event.user.name + "\> ") + content)
    else
      Channel(irc_channel).send(Format(@colours.sample(random: Random.new(event.user.id.to_i)), "\<" + event.user.name + "\> ") + event.message.attachments[0].url)
      if !content.empty?
        Channel(irc_channel).send( Format(@colours.sample(random: Random.new(event.user.id.to_i)), "\<" +  event.user.name + "\> ") + content)
      end
    end
  end
end

irc = Thread.new {irc_bot.start}
discord = Thread.new {discord_bot.run}

irc.join