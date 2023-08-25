from Q1_markov_function import life_month_model, difference_calculator_LM
from Q2_markov_function import cost_life_month_model, ICER_calculator, difference_calculator_Cost
from Q3_markov_function import cost_life_month_model_dist

# Q1 ------------------------------------------------------------
screening_reward_total_life_months = life_month_model(n_max_cycles = 660, screen = 1)
no_screening_total_life_months = life_month_model(n_max_cycles = 660, screen = 100)

# Difference in Years and Months
difference_calculator_LM(screening_reward_total_life_months, no_screening_total_life_months)


# Q2 ------------------------------------------------------------
# Create a list of month, cost for each 5 years
list_of_strategies = []
for i in range(0,11):
    globals()['life_month_cost_yr_%d' % (i * 5)] = cost_life_month_model(n_max_cycles = 660, screen = i)
    list_of_strategies.append(cost_life_month_model(n_max_cycles = 660, screen = i))

# Adding "Do Nothing" Strategy (LM = 0, Cost = 0)
list_of_strategies.append([0,0])

# Adding index number (try: enumerate next time)
for i in range(0, len(list_of_strategies)):
    list_of_strategies[i].insert(0,'%d'%(i))
# Note: Do Nothing has index number i == 11

# Sort the list in ascending order of life_months
sorted_list_strategies = sorted(list_of_strategies, key=lambda x:x[1])

# Attempt to estimate ICER and return value
list_of_ICERS = []
for i in range(1, len(list_of_strategies)):
    list_of_ICERS.append(ICER_calculator(sorted_list_strategies[i-1], sorted_list_strategies[i]))

# Remove strategy 5 ~10 and 0
new_list = []
for e in sorted_list_strategies:
    if e[0] not in ('5', '6', '7', '8', '9', '10', '0'):
        new_list.append(e)
new_list_strategies = new_list

# Recalculate the ICER
list_of_ICERS = []
for i in range(1, len(new_list_strategies)):
    list_of_ICERS.append(ICER_calculator(new_list_strategies[i-1], new_list_strategies[i]))
list_of_ICERS

# Remove strategy 4
new_list_strategies
new_list_strategies.remove(new_list_strategies[1])

# Recalculate the ICER
list_of_ICERS = []
for i in range(1, len(new_list_strategies)):
    list_of_ICERS.append(ICER_calculator(new_list_strategies[i-1], new_list_strategies[i]))

# Q3 ------------------------------------------------------------

no_screening_LM_C_Dist = cost_life_month_model_dist(n_max_cycles = 660, screen = 100)
screening_LM_C_Dist = cost_life_month_model_dist(n_max_cycles = 660, screen = 20)

# Difference in Years and Months
difference_calculator_LM(screening_LM_C_Dist[0], no_screening_LM_C_Dist[0])

# Make a for-loop, creating either a Dictionary or List storing all values.
dict_LM = {}
cost_average_upper_lower_95CI = []
for i in range(11):
    cost_life_month_model_dist(n_max_cycles=660, screen=i)

# Difference in Costs
difference_calculator_Cost(screening_LM_C_Dist[3], no_screening_LM_C_Dist[3])