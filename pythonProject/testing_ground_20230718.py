import numpy as np


n_max_cycles = 660
list_of_ticker = []
for t in range(0,n_max_cycles, 60):
    list_of_ticker.append(t)
list_of_ticker
list_of_age_ticker = int((list_of_ticker[2])/60)
list_of_age_ticker

n_max_cycles = 660
switch_counter = 0
screen = 1
for t in range(0, n_max_cycles):
    # SENSITIVITY OF TST TEST will turn on if screening == 1
    if (t // 60) == screen and (t%60) == 0:
        sens_TST = 0.80
    else:
        sens_TST = 0
    if sens_TST == 0.80:
        switch_counter += 1

init_state_prop = np.array([1, 0, 0, 0])
transitionProb = np.array([[p_SS, p_SE, p_SI, p_SD],
                           [p_ES, p_EE, p_EI, p_ED],
                           [p_IS, p_IE, p_II, p_ID],
                           [p_DS, p_DE, p_DI, p_DD]
                                   ])
transitionProb = np.array([[1, 2, 3, 4],
                           [1, 2, 3, 4],
                           [1, 2, 3, 4],
                           [1, 2, 3, 4]
                            ])
end_state_prop = init_state_prop.dot(transitionProb)
end_state_prop = transitionProb.matmul(init_state_prop)
end_state_prop

init_state_prop = np.array([1, 2, 3, 0])
init_state_prop_multi = init_state_prop[0:3] * init_state_prop[0:3]
init_state_prop_multi

c_test = 10
c_total_test = sum(c_test * init_state_prop[0:3])


def test_function(x):
    w = 0
    f = 0
    for i in range(x):
        w += 2
        f += 5
    return w,f

test_function(10)

end_state_prop = np.array([-1, 2, 3, -2])
for x in end_state_prop:
    if x <0:
        abs(np.ndarray.item(end_state_prop[np.where(end_state_prop == x)])))


for index, x in enumerate(end_state_prop):
    if x <0:
        end_state_prop[index] = 0

end_state_prop

sens_TST = 0.8
false_positive_TST = 0.05
p_prop_test_positive = np.array([init_state_prop[0] * false_positive_TST,
                                      init_state_prop[1] * sens_TST,
                                      init_state_prop[2] * sens_TST])


print(sum(p_prop_test_positive))


if result[0] == 0:
    list_of_strategies.remove(list_of_strategies[0])



for i in range(0,11):
    list_of_strategies[i].insert(0,'Strategy_%d'%(i))

list_of_ICERS = []
# Attempt to estimate ICER and return value
for i in range(1,11):
    globals()['ICER_Cohort_%d' % (i * 5)] = ICER_calculator(dictionary_of_strategies.get('Strategy_%d'%(i-1)), dictionary_of_strategies.get('Strategy_%d'%(i)))
    list_of_ICERS.append(ICER_calculator(dictionary_of_strategies.get('Strategy_%d'%(i-1)), dictionary_of_strategies.get('Strategy_%d'%(i))))

list_of_ICERS



# Assigning specific value to specific strategy
dict_strategy = {}
for i in range(0,11):
    dict_strategy['%d'%(i)] = list_of_strategies[i]

# Sorting dictionaries by ascending order of health outcomes
sorted_dict_strategy = sorted(dict_strategy.items(), key=lambda x:x[1])

# Converting sorted list into dictionary
converted_dict_strategy = dict(sorted_dict_strategy)
converted_dict_strategy[0]

first_strategy = [1,0]
second_strategy = [2, 0]

x = ['%s'%(f"{first_strategy[0]} vs. {second_strategy[0]}")]
x

if list_of_ICERS[i-1] == 0:
    sorted_list_strategies.remove(sorted_list_strategies[i-1])

    if list_of_ICERS[i-1][1] < 0:
        if list_of_ICERS[i-1][1] == 3:
            remove


ICER_calculator(sorted_list_strategies[1], sorted_list_strategies[0])

new_list = new_list_creator(sorted_list_strategies)

globals()['ICER_Cohort_%d' % (i * 5)] = ICER_calculator(sorted_list_strategies[i-1], sorted_list_strategies[i])

for i in range(1, 12):
    if list_of_ICERS[i][1] == 0:
        sorted_list_strategies.remove(sorted_list_strategies[i])



item_list = ['item', 5, 'foo', 3.14, True]
new_list = []
for e in item_list:
    if e not in ('item', 5):
        new_list.append(e)
item_list = new_list

# above code is equivalent to:
item_list = ['item', 5, 'foo', 3.14, True]
item_list = [e for e in item_list if e not in ('item', 5)]

