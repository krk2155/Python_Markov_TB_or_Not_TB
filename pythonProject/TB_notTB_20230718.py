from Q1_markov_function import life_month_model, difference_calculator
from Q2_markov_function import cost_life_month_model, ICER_calculator


# Q1 ------------------------------------------------------------
screening_reward_total_life_months = life_month_model(n_max_cycles=660, screen = 0)
no_screening_total_life_months = life_month_model(n_max_cycles=660, screen = 100)

# Difference in Years and Months
difference_calculator(screening_reward_total_life_months, no_screening_total_life_months)


# Q2 ------------------------------------------------------------
# Create a list of month, cost for each 5 years
list_of_strategies = []

for i in range(0,11):
    globals()['life_month_cost_yr_%d' % (i*5)] = cost_life_month_model(n_max_cycles=660, screen= i)
    list_of_strategies.append(cost_life_month_model(n_max_cycles=660, screen= i))

"""len(list_of_strategies)
list_of_strategies[0][0]

for i in range(0,11):
    ICER_calculator(list_of_strategies[0])
"""

result = ICER_calculator(list_of_strategies[1], list_of_strategies[0])
result