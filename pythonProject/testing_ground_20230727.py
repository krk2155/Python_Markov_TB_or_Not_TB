import numpy as np
import math

n_max_cycles = 120
screen = 1
total_life_months = 0
total_accum_cost = 0
init_state_prop = np.array([1, 0, 0, 0])


for t in range(60, n_max_cycles):

    # Probability of Background Death
    p_BD = 1 - math.exp(-math.exp(-8 + t / 20) * 1 / 12)

    # Probability of State Transition
    # p(S->E)
    p_SE = 0.00167
    # p(E->I)
    p_EI = 0.0000833
    # p(I->D)
    p_ID = 0.0328
    # p(I->E)
    p_IE = 0.156

    # check for when to screen every 60 months (12 months * 5 years)
    if (t // 60) == screen and (t % 60) == 0:
        sensitivity_screen = 0.80
        false_negative = 1 - sensitivity_screen
        specificity_screen = 0.95
        false_positive = 1 - specificity_screen
        p_SE_T_pos = (sensitivity_screen * p_SE) / ((sensitivity_screen * p_SE) + false_positive * (1 - p_SE))
        p_SE_T_neg = ((1 - sensitivity_screen) * p_SE) / (
                    ((1 - sensitivity_screen) * p_SE) + specificity_screen * (1 - p_SE))
        p_EI_T_neg = ((1 - sensitivity_screen) * p_EI) / (
                    ((1 - sensitivity_screen) * p_EI) + specificity_screen * (1 - p_EI))

        # Probabilities
        p_SE = specificity_screen * p_SE_T_neg  # probability that S --> I AND test correctly says does not have E/I
        p_EI = false_negative * p_EI_T_neg  # probability that E --> I AND test has negative
        p_ES = sensitivity_screen  # among E, tested positive --> becomes S

    else:
        sensitivity_screen = 0
        false_negative = 1 - sensitivity_screen
        specificity_screen = 0
        false_positive = 1 - specificity_screen

        # Probabilities
        p_SE = p_SE
        p_EI = p_EI
        p_ES = 0
        p_IE = p_IE

    # State Transition Probabilities (per 1 month)
    # starting from 'Susceptible' state
    p_SD = p_BD
    p_SI = 0
    p_SE = p_SE
    p_SS = 1 - p_SE - p_SD - p_SI

    # starting from 'Latent TB' state
    p_ED = p_BD
    p_EI = p_EI
    p_ES = p_ES
    p_EE = 1 - p_ED - p_EI - p_ES

    # starting from 'Active TB' state
    p_IS = 0
    p_IE = p_IE
    p_ID = p_ID + p_BD
    p_II = 1 - p_IE - p_ID

    # starting from 'dead' state
    p_DS = 0
    p_DE = 0
    p_DI = 0
    p_DD = 1


    # transition probabilities
    transitionProb = np.array([[p_SS, p_SE, p_SI, p_SD],
                               [p_ES, p_EE, p_EI, p_ED],
                               [p_IS, p_IE, p_II, p_ID],
                               [p_DS, p_DE, p_DI, p_DD]
                               ])

    # multiplying init_state matrix with transitionProb matrix
    end_state_prop = init_state_prop.dot(transitionProb)

    for index, x in enumerate(end_state_prop):
        if x < 0:
            end_state_prop[index] = 0

    # new init_state is the old end_state
    init_state_prop = end_state_prop.copy()

    # add "life-month" of "Susceptible", "Latent TB", and "Active TB" states
    cycle_reward = sum(init_state_prop[0:3])

    # accumulate each cycle's "life-months" into "total_life_months"
    total_life_months += cycle_reward

for i in range(10):
    print(i)

for i in range(10):
    if i == 2:
        print("this value is 2")
    else:
        continue
    print(i)