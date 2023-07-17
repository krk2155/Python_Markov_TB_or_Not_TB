from Q1_markov_function import life_month_model, difference_calculator
"""from Q2_markov_function import cost_life_month_model"""


# Q1 ------------------------------------------------------------
screening_reward_total_life_months = life_month_model(n_max_cycles=660, screen = 3)
no_screening_total_life_months = life_month_model(n_max_cycles=660, screen = 100)

# Difference in Years and Months
difference_calculator(screening_reward_total_life_months, no_screening_total_life_months)


# Q2 ------------------------------------------------------------
#life_cost_screening = cost_life_month_model(n_max_cycles=600, screen=100)




