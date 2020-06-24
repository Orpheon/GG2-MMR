import json
import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import trueskill
import seaborn as sns

sns.set_style("whitegrid")

ROOT = "games"
REGION = ""
BANLIST = ["Piza"]

game_files = os.listdir(ROOT)
ratings = {}
win_loss_ratio = {}
history = pd.DataFrame()
for game_file in sorted(game_files):
  with open(os.path.join(ROOT, game_file), 'r') as f:
    data = json.load(f)['games']
  for game in data:
    if "region" not in game:
      game['region'] = "na"
    if REGION != "" and game['region'] != REGION: continue
    victor_ratings = [ratings.get(v, trueskill.Rating()) for v in game['victors']]
    loser_ratings = [ratings.get(v, trueskill.Rating()) for v in game['losers']]
    new_victor_ratings, new_loser_ratings = trueskill.rate((victor_ratings, loser_ratings), ranks=[0, 1])
    for idx,v in enumerate(game['victors']):
      ratings[v] = new_victor_ratings[idx]
      if v not in win_loss_ratio:
        win_loss_ratio[v] = {"wins": 0, "total": 0}
      win_loss_ratio[v]['wins'] += 1
      win_loss_ratio[v]['total'] += 1
    for idx,v in enumerate(game['losers']):
      if v not in win_loss_ratio:
        win_loss_ratio[v] = {"wins": 0, "total": 0}
      win_loss_ratio[v]['total'] += 1
      ratings[v] = new_loser_ratings[idx]
  new_row = pd.DataFrame(
    index=[game_file.replace(".json", "")],
    columns=list(ratings.keys()) + [k+"_2sigma" for k in ratings.keys()]
  )
  for name,rating in ratings.items():
    new_row[name] = rating.mu
    new_row[name+"_2sigma"] = rating.sigma * 2
  history = pd.concat((history, new_row), join="outer")

for name, rating in sorted(ratings.items(), key=lambda x: x[1].mu, reverse=True):
  if name in BANLIST: continue
  print("{0}: {1} +/- {2} (Win Percentage: {3}%, {4} games)".format(
    name,
    round(rating.mu, 3),
    round(2*rating.sigma, 1),
    int(round(100*win_loss_ratio[name]['wins'] / win_loss_ratio[name]['total'], 0)),
    win_loss_ratio[name]['total']
  ))

# palette = sns.color_palette("husl", len(ratings))
# for idx,name in enumerate(ratings):
#   sns.lineplot(data=history, x=history.index, y=history[name], label=name, palette=palette[idx])
#   lower_bound = history[name] - history[name+"_2sigma"]
#   upper_bound = history[name] + history[name+"_2sigma"]
#   plt.fill_between(history.index, lower_bound, upper_bound, alpha=.3)
# plt.ylabel(None)
# plt.legend()
# plt.show()
