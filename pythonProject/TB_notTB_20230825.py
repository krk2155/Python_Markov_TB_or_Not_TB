from matplotlib import pyplot as plt
from Q1_markov_function_PC import life_month_model, LY_difference
from Q2_markov_function_PC import list_of_sorted_strategy,  print_ICER, strategy_remover
from Q3_markov_function_PC import cost_life_month_model_dist, difference_calculator_Cost
from Q4_markov_function_PC import p_of_CE, WTP_at_1000

# Q1 ------------------------------------------------------------
ls_LY = []
LY = 0
# screening at age 0 ~ 50 y.o.
for i in range(0, 11):
    LY = life_month_model(screen=i)
    ls_LY.append(LY)

# no screening strategy
no_screening = life_month_model(screen=1000)

# List of LY difference between each strategy and no-screening strategy
ls_LY_diff = []
for i in range(0, 11):
    ls_LY_diff.append(LY_difference(ls_LY[i], no_screening))


# Q2 ------------------------------------------------------------
# Create a list of month, cost for each 5 years
list_of_strategies = list_of_sorted_strategy()
list_of_strategies

# Attempt to estimate ICER and return value
list_of_ICERS = print_ICER(list_of_strategies)
list_of_ICERS

# Remove strategy 5 ~ 11 and 2
list_strategy_to_remove = ['5', '6', '7', '8', '9', '10', '11','2']
new_list = strategy_remover(list_of_strategies, list_strategy_to_remove)
new_list

# Recalculate the ICER
list_of_ICERS = print_ICER(new_list)
list_of_ICERS

# Remove strategy 4
new_list.pop(0)
new_list

# Recalculate the ICER
list_of_ICERS = print_ICER(new_list)
list_of_ICERS

# Result of ICERS:
# ICER between strategy "0" vs. "3": 24155503.845547542
# ICER between strategy "1" vs. "0": 48308.625921583174

# Given WTP threshold of $1000/Life-Year, strategy#3 (screening at age 15) is preferred.
# This is different from the result of Question 1, which showed that screening at age 5 produces the most Life-Years


# Q3 ------------------------------------------------------------
ls_LY_cost_95CI = []
LY_cost_95CI = []

# screening at age 0 ~ 50 y.o.
for i in range(0, 11):
    LY_cost_95CI = cost_life_month_model_dist(screen=i)
    ls_LY_cost_95CI.append(LY_cost_95CI)

ls_LY_cost_95CI

# no screening strategy
no_screening = cost_life_month_model_dist(screen=1000)
no_screening

# adding a no-screening strategy to the list of strategies
ls_LY_cost_95CI.append(cost_life_month_model_dist(screen=1000))

# 8/26/2023: start from here - fix the LY/Cost difference between
# each strategy LY and costs.

# Difference in Years and Months
LY_difference(ls_LY_cost_95CI[0][0], no_screening[0])

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
plt.title("Cost-Effectiveness Acceptability Curve (n of simulation = 100)")
plt.savefig('Figure1.png', bbox_inches='tight')
plt.show()



# if WTP == 1000:
WTP_at_1000()

# 99.7% probability that the strategy identified in (b) is optimal at $1000/LY