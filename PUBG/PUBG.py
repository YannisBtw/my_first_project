import json

with open('pubg_players.json', 'r') as f:
    player_stats = json.load(f)

    cheaters = []
    for player in player_stats:
        if player["rideDistance"] == 0 and player["roadKills"] > 0:
            cheaters.append(player["Id"])
    print(cheaters)
    print(len(cheaters))
