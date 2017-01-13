import praw, os, time, datetime, random
from praw.models import Comment



print('Logging in...')
bot = praw.Reddit(user_agent='Congratulations bot by winnie33',
                client_id='nq7w3xLv47wOhw',
                client_secret='LoYfZamTtyRpz_HlPRIzoncNiYo',
                username='You_did_great_bot',
                password='pythonowns')

print('Logged in!')

# a fantastic list of fantastic responses for fantastic people
responses = ['Hey, good job!', "I'm proud of you!", "I knew you could do it!", "Nice!", "You did great!", "Fantastic!",
             "You're the best person in the world!","Amazing, I'm proud of you!", "Impressive!"]

thanks = ['No problem!', "No problem, you're welcome!", "No need to thank me, this is what I was made for.",
          "Glad I could make you happy!", "You're welcome!", "Thanks for thanking me!"]

emoticons = [':D', ':)', ':O', ':P', '^^', '=)', '=D']

lastmessage = 0
loopchecker = 0

if not os.path.isfile('posts_replied_to.txt'):
    posts_replied_to = []
else:
    f = open('posts_replied_to.txt', 'r')
    posts_replied_to = [line.rstrip('\n') for line in f]    # fill the list with earlier submissions to prevent doubles
    f.close()
    print("Got submission id's.")


def getdate(post):          # in case I need it
    time = post.created
    date = datetime.datetime.fromtimestamp(time)
    print(date)


def getmessages():
    unread_messages = 0
    for _ in bot.inbox.unread():
        unread_messages += 1
    return str(unread_messages)


def thankusersback():
    for comment in bot.inbox.unread():
        if isinstance(comment, Comment):
            if 'thank' in comment.body.lower():
                comment.mark_read()
                randomNumber = random.randint(0, 5)
                comment.reply(thanks[randomNumber])
                print('Thanked a thanking user!')
                print('"' + comment.body + '"  |Response: ' + thanks[randomNumber])
            else:
                answerstring = ''
                for emoji in emoticons:
                    if emoji in comment.body:
                        answerstring = answerstring + emoji + ' '
                if answerstring != '':
                    comment.mark_read()
                    comment.reply(answerstring)
                    print("I emoji'd back to someone!")
                    print('"' + comment.body + '"  |Response: ' + answerstring)


while True:
    subreddit = bot.subreddit('congratslikeimfive')
    # print('Checking for new posts...')
    for post in subreddit.new(limit=50):              # get 50 latest new posts
        if post.id not in posts_replied_to:
            randomNumber = random.randint(0, 8)      # get a random response
            post.reply(responses[randomNumber])      # reply with said response
            print('the bot replied to ' + post.url)
            print('Title: ' + post.title + '  response: ' + responses[randomNumber])
            posts_replied_to.append(post.id)
            f = open('posts_replied_to.txt', 'a')
            f.write(post.id + '\n')                  # add the post id to the text file
            f.close()
            # time.sleep(600)                          # wait 10 minutes so you don't get in trouble with reply rate
            break                                    # break out to see newer posts, sorry people we missed ;-;
    # print('Done checking, going to sleep for now.')
    messages = getmessages()
    if messages != lastmessage:
        print('Currently ' + messages + ' messages.')
        lastmessage = messages
        thankusersback()
    time.sleep(20)                                   # another 20 seconds wait
    loopchecker += 1
    if loopchecker % 180 == 0:
        print('Still alive! Currently about ' + str(loopchecker/180) + ' hours active.')





