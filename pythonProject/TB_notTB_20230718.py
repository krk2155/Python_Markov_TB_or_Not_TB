from Q1_markov_function import life_month_model, difference_calculator
from Q2_markov_function import cost_life_month_model, ICER_calculator


# Q1 ------------------------------------------------------------
screening_reward_total_life_months = life_month_model(n_max_cycles = 660, screen = 0)
no_screening_total_life_months = life_month_model(n_max_cycles = 660, screen = 100)

# Difference in Years and Months
difference_calculator(screening_reward_total_life_months, no_screening_total_life_months)


# Q2 ------------------------------------------------------------
# Create a list of month, cost for each 5 years
list_of_strategies = []
for i in range(0,11):
    globals()['life_month_cost_yr_%d' % (i * 5)] = cost_life_month_model(n_max_cycles = 660, screen = i)
    list_of_strategies.append(cost_life_month_model(n_max_cycles = 660, screen = i))

list_of_strategies.append([0,0])
list_of_strategies


for i in range(0, len(list_of_strategies)):
    list_of_strategies[i].insert(0,'%d'%(i))
# Note: Do Nothing has i == 11

# Sort the list in ascending order of life_months
sorted_list_strategies = sorted(list_of_strategies, key=lambda x:x[1])
sorted_list_strategies

# Attempt to estimate ICER and return value
list_of_ICERS = []
for i in range(1, len(list_of_strategies)):
    list_of_ICERS.append(ICER_calculator(sorted_list_strategies[i-1], sorted_list_strategies[i]))

list_of_ICERS

# Remove strategy 5 ~10 and 0
new_list = []
for e in sorted_list_strategies:
    if e[0] not in ('5', '6', '7', '8', '9', '10', '0'):
        new_list.append(e)
new_list_strategies = new_list
len(new_list_strategies)


# Recalculate the ICER
list_of_ICERS = []
for i in range(1, len(new_list_strategies)):
    list_of_ICERS.append(ICER_calculator(new_list_strategies[i-1], new_list_strategies[i]))

# Remove strategy 2
new_list_strategies.remove(new_list_strategies[3])
new_list_strategies


# Recalculate the ICER
list_of_ICERS = []
for i in range(1, len(new_list_strategies)):
    list_of_ICERS.append(ICER_calculator(new_list_strategies[i-1], new_list_strategies[i]))
list_of_ICERS


# Q3 ------------------------------------------------------------

