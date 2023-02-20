# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:53:42 2023

@author: 20192020
"""
import matplotlib.pyplot as plt 
import numpy as np 
import pickle
import seaborn as sns 
from scipy import stats
import random 
import os 

os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir)) # go one folder back
import assignment_1.constants as c

plt.style.use('ggplot') # plotting style 

#%% Gather data
all_files = [10, 15, 25, 50, 75, 100, 250, 500, 750, 1000] #, 10000]
all_statistics = [0]*len(all_files)

for i in range(len(all_statistics)):
    nr = all_files[i]
    file = f"assignment_1\data\statistics_nruns={nr}.pkl"
    all_statistics[i] = pickle.load(open(file, 'rb'))
    
    
white_probs = np.zeros((len(all_statistics),))
black_probs = np.zeros((len(all_statistics),))
draw_probs = np.zeros((len(all_statistics),))
CIup_white = np.zeros((len(all_statistics),))
CIup_black = np.zeros((len(all_statistics),))
CIup_draw = np.zeros((len(all_statistics),))
CIlow_white = np.zeros((len(all_statistics),))
CIlow_black = np.zeros((len(all_statistics),))
CIlow_draw = np.zeros((len(all_statistics),))

for i in range(len(all_statistics)):
    stat = all_statistics[i]
    white_probs[i] = stat['white_wins_prop']
    black_probs[i] = stat['black_wins_prop']
    draw_probs[i] = stat['draws_prop']
    
    CIup_white[i] = stat['white_wins_normal_ci_95'][0]
    CIup_black[i] = stat['black_wins_normal_ci_95'][0]
    CIup_draw[i] = stat['draws_normal_ci_95'][0]
    CIlow_white[i] = stat['white_wins_normal_ci_95'][1]
    CIlow_black[i] = stat['black_wins_normal_ci_95'][1]
    CIlow_draw[i] = stat['draws_normal_ci_95'][1]

#%% Plotting confidence intervals  
plt.figure()
plt.close('all')
#fig, ax = plt.subplots(1, 3)

#ax[0].plot(all_files, white_probs)
plt.plot(all_files, white_probs, marker = '.')
plt.plot(all_files, black_probs, marker = '.')
plt.plot(all_files, draw_probs, marker = '.')

plt.fill_between(all_files, CIlow_white, CIup_white, alpha =.2)
plt.fill_between(all_files, CIlow_black, CIup_black, alpha =.25)
plt.fill_between(all_files, CIlow_draw, CIup_draw, alpha =.2)

plt.xlabel('Number of runs')
plt.ylabel('Probability')
plt.title('Probabilities and confidence intervals for match outcomes')
plt.legend(['White wins', 'Black wins', 'Draw'])
    
#%% Bootstrapping
#plt.close('all')

file = "assignment_1\data\statistics_nruns=10000.pkl"
stats_10000 = pickle.load(open(file, 'rb'))
results = stats_10000['results']
winner_results = results[results != 3] 

# create binary columns 
white_winning = abs(winner_results - np.ones(np.shape(winner_results))*2)
black_winning = winner_results - np.ones(np.shape(winner_results))

means_white = np.zeros((10000,))
means_black = np.zeros((10000,))
for i in range(10000):
    mean_w = np.mean(random.choices(white_winning, k=len(white_winning)))
    mean_b = np.mean(random.choices(black_winning, k=len(black_winning)))
    means_white[i] = mean_w
    means_black[i] = mean_b
    
#%% Plot histograms 
fig, ax = plt.subplots()
binwidth = 10
sns.histplot(means_white, kde=True, bins=int(180/binwidth), ax=ax, color='red')
sns.histplot(means_black, kde=True, bins=int(180/binwidth), ax=ax)
ax.legend(['White wins', 'Black wins'])
ax.set_xlabel('Probability')
ax.set_title('Winning probability per color')

#%% Hypothesis test 
ttest,pval = stats.ttest_rel(white_winning, black_winning)
print(pval)
if pval<0.05:
    print("reject null hypothesis")
else:
    print("accept null hypothesis")
    
#%% Get game_history of 10000 runs
nr = 10000
#os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
file = f"assignment_1\data\game_history_nruns={nr}.pkl"
game_history = pickle.load(open(file, 'rb'))

#%% Gather data about rounds 
all_runs = game_history.get_game_runs()

# queen promotion 
prom_per_match = []
prom_white_wins = []
prom_black_wins = []
prom_draw = []

# number of rounds 
r_white = []
r_black = []
r_draw = []
rounds = all_statistics[-1]['rounds_per_match']

for i in range(game_history.games_played):
    run = all_runs[i]
    queen_prom = run.chess_board.n_queen_promotions
    prom_per_match.append(queen_prom)
    
    state = run.get_game_state() 
    if state == c.GameStates.WHITE_WON:
        prom_white_wins.append(queen_prom)
        r_white.append(rounds[i])
    elif state == c.GameStates.BLACK_WON:
        prom_black_wins.append(queen_prom)
        r_black.append(rounds[i])
    else:
        prom_draw.append(queen_prom)
        r_draw.append(rounds[i])
        
#%% Used function from simulator to calculate confidence intervals for rounds
conf_to_z = {
    0.90: 1.645,
    0.95: 1.960,
    0.99: 2.576,
}

def CI_N(
    n: int, u: np.float32, var: np.float32, alpha: float
) -> tuple:
    """
    Computes the confidence interval for a normal distribution.

    :param n: The number of trials.
    :param u: The mean.
    :param var: The variance.
    :param alpha: The significance level.
    :return: The confidence interval.
    """

    # assume a normal distr. and get the confidence interval for the mean
    z = conf_to_z[alpha]
    u_up = np.round(u + z * np.sqrt(var / n), 3)
    u_low = np.round(u - z * np.sqrt(var / n), 3)

    # return the confidence interval
    return (u_low, u_up)

CI95_total = CI_N(len(rounds), np.mean(rounds), np.var(rounds), 0.95)
CI95_white = CI_N(len(r_white), np.mean(r_white), np.var(r_white), 0.95)
CI95_black = CI_N(len(r_black), np.mean(r_black), np.var(r_black), 0.95)
CI95_draw = CI_N(len(r_draw), np.mean(r_draw), np.var(r_draw), 0.95)

        
#%% Plot boxplots for queen promotions 
plt.figure()
plt.boxplot([prom_per_match, prom_white_wins, prom_black_wins, prom_draw])
plt.xticks(range(1, 5), ['All matches', 'White won', 'Black won', 'Draw'])
plt.ylabel('Count')
plt.title('Number of queen promotions per game')             
             
