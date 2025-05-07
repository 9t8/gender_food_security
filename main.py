import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('Results.csv')

foodsec_key = 'Column_Variable_Value'
foodsec_values = [*map(str, range(4, 0, -1))]
foodsec_names = [*(df[df[foodsec_key] == i]
                   ['Column_Variable_Value_Label'].iloc[0]
                   for i in foodsec_values)]
foodsec_colors = ('r', 'y', 'g', 'b')

gender_key = 'Row_Variable_Value'
gender_values = [*map(str, range(1, 4))]
gender_names = [*(df[df[gender_key] == i]
                  ['Row_Variable_Value_Label'].iloc[0]
                  for i in gender_values)]

income_key = 'Subtable_Variable_Value'
income_values = [*map(str, range(1, 30))]
income_names = [*(df[df[income_key] == i]
                  ['Subtable_Variable_Value_Label'].iloc[0]
                  for i in income_values)]

df = df.assign(val=df['Estimate'].map(
    lambda x: float(x.strip('!').replace('‡', '0'))))

for gender_value in gender_values:
    for income_value in income_values:
        mask = (df[gender_key] == gender_value) & (
            df[income_key] == income_value) & (
            df[foodsec_key].isin(foodsec_values))
        vals = df.loc[mask, 'val']
        if np.count_nonzero(vals) == 3:
            df.loc[mask & (df['val'] == 0), 'val'] = 100 - vals.sum()

x = np.arange(len(income_values))
width = .25
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for gender_value, gender_name in zip(gender_values, gender_names):
    bottom = np.zeros(len(income_values))

    for foodsec_value, foodsec_name, foodsec_color in zip(
            foodsec_values, foodsec_names, foodsec_colors):
        vals = df[(df[foodsec_key] == foodsec_value) &
                  (df[gender_key] == gender_value)].set_index(income_key)[
            'val'].reindex(income_values).to_numpy()

        ax.bar(
            x + width * multiplier, vals, width,
            label=f'{gender_name[0]}, {foodsec_name[:-len(" food security")]}',
            bottom=bottom,
            color=(foodsec_color, width * (multiplier + 2))
        )
        bottom += vals

    multiplier += 1

ax.set_xlabel('income')
ax.set_ylabel('food security (%)')
ax.set_title('Food security by income and gender')
ax.set_xticks(x + width * (len(gender_values) - 1) /
              2, income_names, rotation=90)
ax.legend(ncols=len(gender_values))

plt.show()
