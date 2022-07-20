import tweepy
import csv

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


csvfile = open('home/user/ubuntu/mlb-hit-well-bot/data/tweets.csv', 'r', encoding='utf-8')
reader = csv.reader(csvfile, delimiter=',')

lines = list(reader)
csvfile.close()

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
api = tweepy.API(auth, wait_on_rate_limit=True)

n = 0

for line in lines:
    if line[1] == 'False':
        print('Tweet has not yet been sent. Creating tweet')
        picture = api.media_upload('home/user/ubuntu/mlb-hit-well-bot/images/' + line[3]) 
        mediaID = picture.media_id
        try:
            response = client.create_tweet(
                text=str(line[2]),
                media_ids=[mediaID]
            )
            print(f"https://twitter.com/user/status/{response.data['id']}")
            lines[n][1] = 'True'
        
            csvfile = open('home/user/ubuntu/mlb-hit-well-bot/data/tweets.csv', 'w', encoding='utf-8', newline="")    
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(lines)
            csvfile.close()
        except:
            print("Reached tweet limit. Will try again later.")
    n+=1

