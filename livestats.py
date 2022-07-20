import datetime
import statsapi
import csv
from hitwell import PrepareTweet, PreparePlot

today = datetime.datetime.today() - datetime.timedelta(hours=9)
date = today.strftime('%Y-%m-%d')

# yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
# yesterdaysDate = yesterday.strftime('%Y-%m-%d')

sched = statsapi.schedule(date=date)

# gameIDs = [663083] # test gameID
gameIDs = []
for g in sched:
    gameIDs += [g.get("game_id")]

csv.QUOTE_ALL

for id in gameIDs:
    pbp = statsapi.get('game_playByPlay', {'gamePk':id})
    for play in pbp.get('allPlays'):
        for event in play.get('playEvents'):
            # only collect index and launch speed if ball is hit in play
            if type(event.get('hitData')) is dict:
                # get launch speed from hitData for event
                launchSpeed = event.get('hitData').get('launchSpeed')

                if launchSpeed is not None and launchSpeed >= 100:
                    # get data of event
                    playId = event.get('playId')
                    abIndex = play.get('atBatIndex')
                    launchAngle = event.get('hitData').get('launchAngle')
                    totalDistance = event.get('hitData').get('totalDistance')
                    pitchSpeed = event.get('pitchData').get('startSpeed')
                    pitchType = event.get('details').get('type').get('description')
                    outcome = play.get('result').get('event')
                    eventType = play.get('result').get('eventType')
                    batter = play.get('matchup').get('batter').get('fullName')
                    pitcher = play.get('matchup').get('pitcher').get('fullName')
                    hTeam = statsapi.schedule(game_id=id)[0].get('home_name')
                    aTeam = statsapi.schedule(game_id=id)[0].get('away_name')
                    hScore = play.get('result').get('homeScore')
                    aScore = play.get('result').get('awayScore')
                    outs = play.get('count').get('outs')
                    inning = play.get('about').get('inning')
                    top = play.get('about').get('isTopInning')
                    xCoord = float(event.get('hitData').get('coordinates').get('coordX'))
                    yCoord = float(event.get('hitData').get('coordinates').get('coordY'))

                    eventData = {
                        'playId': playId,
                        'gamePk': id,
                        'abIndex': abIndex,
                        'launchSpeed': launchSpeed,
                        'launchAngle': launchAngle,
                        'totalDistance': totalDistance,
                        'pitchSpeed': pitchSpeed,
                        'pitchType': pitchType,
                        'outcome': outcome,
                        'eventType': eventType,
                        'batter': batter,
                        'pitcher': pitcher,
                        'hTeam': hTeam,
                        'aTeam': aTeam,
                        'hScore': hScore,
                        'aScore': aScore,
                        'outs': outs,
                        'inning': inning,
                        'top': top,
                        'xCoord': xCoord,
                        'yCoord': yCoord,
                    }
                

                    csvfile = open('home/user/ubuntu/mlb-hit-well-bot/data/tweets.csv', 'r', encoding='utf-8')
                    reader = csv.reader(csvfile, delimiter=',')
                    collected = False
                    for row in reader:
                        if row[0] == playId:
                            collected = True
                    csvfile.close()

                    if not collected:
                        PreparePlot(eventData)  
                        csvfile = open('home/user/ubuntu/mlb-hit-well-bot/data/tweets.csv', 'a', newline="", encoding='utf-8')
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([str(playId), 'False', PrepareTweet(eventData)[0], str(playId) + '.png'])
                        csvfile.close()