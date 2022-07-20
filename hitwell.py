def PrepareTweet(data):
    batter = str(data.get('batter'))
    pitcher = str(data.get('pitcher'))
    launchSpeed = str(data.get('launchSpeed'))
    launchAngle = str(data.get('launchAngle'))
    distance = str(data.get('totalDistance'))
    pitchSpeed = str(data.get('pitchSpeed'))
    pitchType = str(data.get('pitchType'))
    outcome = str(data.get('outcome'))
    hTeam = str(data.get('hTeam'))
    aTeam = str(data.get('aTeam'))
    hScore = str(data.get('hScore'))
    aScore = str(data.get('aScore'))
    outs = str(data.get('outs'))
    inning = str(data.get('inning'))
    # "top" or "bottom" of inning
    if data.get('top'):
        top = 'Top'
    else:
        top = 'Bottom'

    tweet = [batter + " off of " + pitcher + "\r\n\r\n" + "EV🔥: " + launchSpeed  + "\r\nLaunch angle📐: " + launchAngle + " degrees\r\n" + "Pitch type🎨: " + pitchType + "\r\nPitch speed🚄: " + pitchSpeed + " mph\r\n" + "Distance📏: " + distance + " ft." + "\r\nOutcome🙋: " + outcome + "\r\n\r\n" + aTeam + "(" + aScore + ") @ " + hTeam + "(" + hScore + ")\r\n" + top + " " + inning + "  " + outs + " Out"]

    return tweet


def PreparePlot(data):
    stadium = GetStadiumName(data.get('gamePk'))
    playId = data.get('playId')
    data = [[data.get('eventType'), data.get('xCoord'), data.get('yCoord')]]
    import pandas as pd
    data = pd.DataFrame(data, columns=['events', 'hc_x', 'hc_y'])
    import plotting
    illustration = plotting.spraychart(data=data, team_stadium=stadium, size=75)
    plotName = 'home/user/ubuntu/mlb-hit-well-bot/images/' + playId + '.png'
    # plotName = 'home/user/ubuntu/mlb-hit-well-bot/images/' + playId + '.png'
    illustration.savefig(plotName)

    return [plotName]


def GetStadiumName(gamePk):
    import statsapi
    homeID = statsapi.schedule(game_id=gamePk)[0].get('home_id')
    clubName = statsapi.get('team', {'teamId': homeID}).get('teams')[0].get('clubName')
    # teamNames = ['angels', 'astros', 'athletics', 'blue_jays', 'braves', 'brewers', 'cardinals', 'cubs', 'diamondbacks', 'dodgers', 'giants', 'indians', 'mariners', 'marlins', 'mets', 'nationals', 'orioles', 'padres', 'phillies', 'pirates', 'rangers', 'rays', 'red_sox', 'reds', 'rockies', 'royals', 'tigers', 'twins', 'white_sox', 'yankees']
    if clubName == 'Guardians':
        stadiumName = 'indians'
    elif clubName == 'Red Sox':
        stadiumName = 'red_sox'
    elif clubName == 'White Sox':
        stadiumName = 'white_sox'
    elif clubName == "Blue Jays":
        stadiumName = 'blue_jays'
    else: 
        stadiumName = clubName.lower()

    return stadiumName