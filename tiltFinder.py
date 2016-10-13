import json
import urllib2
api_key = 'YOUR_API_KEY_HERE'

def getWinCount(summonerId):

    HISTORY_URL = 'https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/' + str(summonerId) + '/recent?api_key=' + api_key
    history = urllib2.urlopen(HISTORY_URL);
    history_html = history.read();
    history_data = json.loads(history_html);

    games = history_data['games']

    wins = 0;
    for x in games:
        if x['stats']['win']:
            wins = wins + 1;
    return wins;

def getTiltMeter(losses):

    losses = losses * 10
    meter = 0
    tilt = ''
    while meter < losses:
        meter = meter + 1
        tilt = tilt + '|'
    return tilt.strip()

def getChampionNameById(championId):
    CHAMP_URL = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(championId) + '?api_key=' + api_key
    try:
        champ = urllib2.urlopen(CHAMP_URL);
    except urllib2.HTTPError, e:
        return -1;
    else:
        champ_html = champ.read();
        champ_data = json.loads(champ_html);
        return champ_data['name'];

def getTiltedList():
    summoner_name = raw_input('Enter your summoner name:\n')
    summoner_name_formatted = summoner_name.replace(" ", "")
    summoner_name_formatted = summoner_name_formatted.lower()
    URL = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + summoner_name_formatted + '?api_key=' + api_key
    try:
        response = urllib2.urlopen(URL);
    except urllib2.HTTPError, e:
        print('\n' + summoner_name + ' is not a valid summoner name.\n')
        exit()
    else:
        html = response.read();
        data = json.loads(html);
        summoner_id = data[summoner_name_formatted]['id']

    GAME_URL = 'https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/'+ str(summoner_id) + '?api_key=' + api_key
    try:
        current_game = urllib2.urlopen(GAME_URL);
    except urllib2.HTTPError, e:
        print('\n' + summoner_name + ' is not in a game right now.\n')
        exit()
    else:
        html2 = current_game.read();
        data2 = json.loads(html2);
        participants = data2['participants']

    summoner_team = 0;
    for x in participants:
        if x['summonerId'] == summoner_id:
            summoner_team = x['teamId']

    enemy_team = [];
    for y in participants:
        if y['teamId'] != summoner_team:
            playerWins = getWinCount(y['summonerId']);
            enemy_team.append({'Name': y['summonerName'], 'Wins': playerWins, 'championId': y['championId']});

    minWins = 10
    most_tilted = [];
    for item in enemy_team:
        if item['Wins'] < minWins:
            most_tilted = item
            minWins = item['Wins']

    print('\n\tSummoner\t\t|\tChampion\t\t\t|\tTilt Meter')
    print('-----------------------------------------------------------------------------------------------------')
    for item in enemy_team:
        player_name = item['Name']
        player_champion = getChampionNameById(item['championId'])
        player_tilt = getTiltMeter(10 - item['Wins'])
        print '\t{0:16}\t|\t{1:16}\t\t|\t{2:16}'.format(player_name, player_champion, player_tilt)
    print('\n')

getTiltedList();
