import json
import os
import datetime as dt

def define_team(team_prefix):
  players = []
  while True:
    player = input(team_prefix+": ")
    if player == "":
      return players
    else:
      players.append(player)

today = dt.date.today()
today_str = today.strftime(("%Y%m%d"))
red = define_team("Red")
blue = define_team("Blue")
print("Teams:")
print("\tRed:")
print("\n".join("\t\t"+p for p in red))
print("\tBlue:")
print("\n".join("\t\t"+p for p in blue))

region = input("Region: ")
if region == "":
  region = "eu"

games = []
while True:
  map = input("Map: ")
  if map == "":
    break
  winner = input("\tWinner: ")
  if winner == 'r':
    games.append({
      "map": map,
      "victors": red,
      "losers": blue,
      "region": region
    })
  elif winner == 'b':
    games.append({
      "map": map,
      "victors": blue,
      "losers": red,
      "region": region
    })
  else:
    print("Wrong input, use 'r' or 'b' to denote the winner.")

path = os.path.join("games", today_str+".json")
if os.path.exists(path):
  with open(path, "r") as f:
    preload = json.load(f)
    games = preload + games

with open(path, "w") as f:
  json.dump({"games": games}, f, sort_keys=True, indent=2)