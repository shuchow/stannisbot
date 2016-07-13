# stannisbot - What in the world is this?

This is a weechat script to correct a person's improrper usage of "less."  Using weechat (http://www.weechat.org) it monitors a Slack or IRC channel to see if someone needs to be corrected.  It uses Python's textblob NLP library to determine if the word after "less" is a noun, and then an abstract noun whitelist/blacklist to determine if correction is needed.

#Why???

I wanted to build a bot to correct my coworkers in our Slack channel.

#Why not just use a webhook?

A Slack webhook requires a server somewhere to run the bot.  This is problematic for me.  At work, we isolate clients, so I can't run the bot on the network.  I *could* run the bot outside of the network, but it'd be bad form to send company conversations across the internet.

Weechat, though, works as just another Slack client.  You can write a script to process the incoming message buffer and send messages on the buffer.

#How do I use it?

1. Install Weechat.
2. Install the textblob python library system-wide for your default Python version.  (sudo pip install textblob).  Weechat cannot run scripts from a virtualenv sandbox.
3. Follow Calle Erlandsson's instructions (https://robots.thoughtbot.com/weechat-for-slacks-irc-gateway) for "Connecting to Slack"
4. Download the script (stannsibot.py) and the abstract/concrete nouns list.
5. Configure the script with the absolute paths to the abstract and concrete nouns (lines 13 and 14) override the log directory if desired (line 116).
6. Fire up weechat.
7. Join a channel (/join #random)
8. Register stannisbot! (/script load path/to/stannisbot.py)
9. Profit!  Get booed at by coworkers!
