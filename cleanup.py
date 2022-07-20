import csv
import os

csvfile = open('home/user/ubuntu/mlb-hit-well-bot/data/tweets.csv', 'r', encoding='utf-8')
reader = csv.reader(csvfile, delimiter=',')
for row in reader:
    assert row[1] == "True"
csvfile.close()

csvfile = open('home/user/ubuntu/mlb-hit-well-bot/data/tweets.csv', 'w', encoding='utf-8', newline="")    
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(['playId','tweeted','tweet_text','image'])
csvfile.close()
 
dir = 'home/user/ubuntu/mlb-hit-well-bot/images'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))