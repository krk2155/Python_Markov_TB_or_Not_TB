from matplotlib import pyplot as plt

from Q1_markov_function_PC import life_month_model, difference_calculator_LM
from Q2_markov_function_PC import cost_life_month_model, ICER_calculator, difference_calculator_Cost
from Q3_markov_function_PC import cost_life_month_model_dist
from Q4_markov_function_PC import p_of_CE, WTP_at_1000

# Q1 ------------------------------------------------------------
screening_reward_total_life_months = life_month_model(n_max_cycles=660, screen=1)
no_screening_total_life_months = life_month_model(n_max_cycles=600, screen=100)

# Difference in Years and Months
difference_calculator_LM(screening_reward_total_life_months, no_screening_total_life_months)

# Q2 ------------------------------------------------------------
# Create a list of month, cost for each 5 years
list_of_strategies = []
for i in range(0, 11):
    globals()['life_month_cost_yr_%d' % (i * 5)] = cost_life_month_model(n_max_cycles=660, screen=i)
    list_of_strategies.append(cost_life_month_model(n_max_cycles=660, screen=i))

len(list_of_strategies)
list_of_strategies

# Adding "Do Nothing" Strategy (LM & Cost when screening is done at age 500 (never done))
list_of_strategies.append(cost_life_month_model(n_max_cycles=660, screen=1000))

# Adding index number (try: enumerate next time)
# Note: Do Nothing has index number i == 11
for i in range(0, len(list_of_strategies)):
    list_of_strategies[i].insert(0, '%d' % (i))


# Sort the list in ascending order of life_months
sorted_list_strategies = sorted(list_of_strategies, key=lambda x: x[1])
sorted_list_strategies

# Attempt to estimate ICER and return value
list_of_ICERS = []
for i in range(1, len(list_of_strategies)):
    list_of_ICERS.append(ICER_calculator(sorted_list_strategies[i - 1], sorted_list_strategies[i]))
list_of_ICERS

# Remove strategy 5 ~10 and 1
new_list = []
for e in sorted_list_strategies:
    if e[0] not in ('5', '6', '7', '8', '9', '10', '11','2'):
        new_list.append(e)
new_list_strategies = new_list
new_list_strategies

# Recalculate the ICER
list_of_ICERS = []
for i in range(1, len(new_list_strategies)):
    list_of_ICERS.append(ICER_calculator(new_list_strategies[i - 1], new_list_strategies[i]))
list_of_ICERS

new_list_strategies.pop(0)
new_list_strategies

list_of_ICERS = []
for i in range(1, len(new_list_strategies)):
    list_of_ICERS.append(ICER_calculator(new_list_strategies[i - 1], new_list_strategies[i]))
list_of_ICERS

# Result of ICERS:
# ICER between strategy "0" vs. "3": 24155503.845547542
# ICER between strategy "1" vs. "0": 48308.625921583174

############################ ANSWER ###################################
# Given WTP threshold of $1000/Life-Year, strategy#3 is preferred.
# Strategy#3 is to conduct TST screening at age 15.
# This is different from the result of Question 1,
# which showed that screening at age 5 produces the most Life-Years

# Q3 ------------------------------------------------------------
screening_LM_C_Dist = cost_life_month_model_dist(n_max_cycles=660, screen=1)
no_screening_LM_C_Dist = cost_life_month_model_dist(n_max_cycles=660, screen=100)

# Difference in Years and Months
difference_calculator_LM(screening_LM_C_Dist[0], no_screening_LM_C_Dist[0])

# Make a for-loop, creating either a Dictionary or List storing all values.
dict_LM = {}
cost_average_upper_lower_95CI = []
for i in range(11):
    total_outcomes = cost_life_month_model_dist(n_max_cycles=660, screen=i)

# Difference in Costs
difference_calculator_Cost(screening_LM_C_Dist[3], no_screening_LM_C_Dist[3])

# Q4 ------------------------------------------------------------

# making a dataframe for plotting (refer to "Q4_markov_function_PC")
df = p_of_CE()

# plotting the graph (X = WTP, Y = outcome)
plt.plot(df.WTP,df.Probability)
plt.xlabel("WTP")
plt.ylabel("Probability of Cost-Effectiveness")
plt.title("Cost-Effectiveness Acceptability Curve")
plt.show()

# if WTP == 1000:
WTP_at_1000()

# 99.7% probability that the strategy identified in (b) is optimal at $1000/LY