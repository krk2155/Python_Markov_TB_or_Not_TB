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

init_state_prop = np.array([1, 0, 0, 0])
c_test = 10
c_total_test = sum(c_test * init_state_prop[0:3])
c_total_test


end_state_prop = np.array([-1, 2, 3, -2])
for x in end_state_prop:
    if x <0:
        abs(np.ndarray.item(end_state_prop[np.where(end_state_prop == x)])))


        # I NEED TO REPLACE A NEGATIVE ITEM IN END_STATE_PROP ARRAY WITH 0!!!