from matplotlib import pyplot as plt
from Q1_markov_function_PC import list_strategy_generator, list_diff_generator
from Q2_markov_function_PC import list_of_sorted_strategy,  print_ICER, strategy_remover
from Q3_markov_function_PC import list_of_LY_cost_95CI
from Q4_markov_function_PC import p_of_CE, WTP_at_1000

# Q1 ------------------------------------------------------------
# create a list of life-years for each strategy and a life-year of no screening
list_of_strategies, no_screening = list_strategy_generator()
# check
list_of_strategies
#check
no_screening

# calculate the difference between each strategy and no-screening & store in a list
list_of_difference = list_diff_generator(list_of_strategies, no_screening)
# check
list_of_difference

# Q2 ------------------------------------------------------------
# Create a list of month, cost for each 5 years
list_of_strategies = list_of_sorted_strategy()
# check
list_of_strategies

# Attempt to estimate ICER and return value
list_of_ICERS = print_ICER(list_of_strategies)
# check
list_of_ICERS

# Remove strategy 5 ~ 11 and 2
list_strategy_to_remove = ['5', '6', '7', '8', '9', '10', '11','2']
new_list = strategy_remover(list_of_strategies, list_strategy_to_remove)
# check
new_list

# Recalculate the ICER
list_of_ICERS = print_ICER(new_list)
# check
list_of_ICERS

# Remove strategy 4
new_list.pop(0)
# check
new_list

# Recalculate the ICER
list_of_ICERS = print_ICER(new_list)
# check
list_of_ICERS

# Result of ICERS:
# ICER between strategy "0" vs. "3": 24155503.845547542
# ICER between strategy "1" vs. "0": 48308.625921583174

# Given WTP threshold of $1000/Life-Year, strategy#3 (screening at age 15) is preferred.
# This is different from the result of Question 1, which showed that screening at age 5 produces the most Life-Years


# Q3 ------------------------------------------------------------
# create a list of life years and costs and their 95% CI
list_of_LY_cost = list_of_LY_cost_95CI()
list_of_LY_cost


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