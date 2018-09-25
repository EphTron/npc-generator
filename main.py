# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

import random as rand

names_m = list(pd.read_json('name-lists/male_names.json').names)
names_f = list(pd.read_json('name-lists/female_names.json').names)
nick_names = list(pd.read_json('name-lists/nicknames.json').names)
surnames = list(pd.read_json('name-lists/surnames-worldwide.json').names)

friend_name = rand.choice(names_m)
friend_nick_name = rand.choice(nick_names)
friend_surname = rand.choice(surnames)

print(friend_name, friend_nick_name, friend_surname)

helpful = rand.randint(1, 10)
law_abiding = rand.randint(1, 10)
sincerity = rand.randint(1, 10)
tolerance = rand.randint(1, 10)
resilience = rand.randint(1, 10)

# Set data
df = pd.DataFrame({
    'group': ['A'],
    'Hilfsbereitschaft': [helpful],
    'Gesetzestreue': [law_abiding],
    'Aufrichtigkeit': [sincerity],
    'Toleranz': [tolerance],
    'Belastbarkeit': [resilience]
})

# ------- PART 1: Create background

# number of variable
categories = list(df)[0:-1]

# categories = list(df)[0:]
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([0, 2, 4, 6, 8, 10], ["", "2", "4", "6", "8", "10"], color="grey", size=7)
plt.ylim(0, 10)

# ------- PART 2: Add plots

# Plot each individual = each line of the data
# I don't do a loop, because plotting more than 3 groups makes the chart unreadable

# Ind1

values = df.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid')
ax.fill(angles, values, 'b', alpha=0.1)

# Ind2
# values = df.loc[1].drop('group').values.flatten().tolist()
# values += values[:1]
# ax.plot(angles, values, linewidth=1, linestyle='solid', label="group B")
# ax.fill(angles, values, 'r', alpha=0.1)

# Add legend
# plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()

# https://python-graph-gallery.com/392-use-faceting-for-radar-chart/ find other rader diagrams
