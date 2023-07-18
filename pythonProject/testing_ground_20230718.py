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