from Q1_markov_function import life_month_model, difference_calculator
from Q2_markov_function import cost_life_month_model, ICER_calculator, new_list_creator


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

# Sort the list in ascending order of life_months
sorted_list_strategies = sorted(list_of_strategies, key=lambda x:x[0])

list_of_ICERS = []
# Attempt to estimate ICER and return value
for i in range(1,11):
    globals()['ICER_Cohort_%d' % (i * 5)] = ICER_calculator(sorted_list_strategies[i-1], sorted_list_strategies[i])
    list_of_ICERS.append(ICER_calculator(sorted_list_strategies[i-1], sorted_list_strategies[i]))
list_of_ICERS
ICER_calculator(sorted_list_strategies[1], sorted_list_strategies[0])

new_list = new_list_creator(sorted_list_strategies)

# NEED TO FIX THE new_list_creator
# NEED TO INTERPRETE THE RESULT OF LIST_OF_ICERS
