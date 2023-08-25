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

    # cost estimates
    c_test = 10
    c_treatment = 200

    # Check When to Screen Every 60 Months (12 months * 5 years)
    if (t // 60) == screen and (t % 60) == 0:
        # Check When to Screen Every 60 Months (12 months * 5 years)
        if (t // 60) == screen and (t % 60) == 0:
            # Tested & Treated:
            sensitivity_screen = 0.80
            specificity_screen = 0.95

            # New Probability of Disease Progression
            # [assuming mutual exclusivity between p_EI and positive test results]
            p_SE = p_SE - specificity_screen
            p_EI = p_EI - (1 - sensitivity_screen)
            p_IE = p_IE + sensitivity_screen

            # Cost of Being Tested Positive and Treated
            # proportion of those being tested positive
            p_prop_test_positive = np.array([init_state_prop[0] * (1 - specificity_screen),
                                             init_state_prop[1] * sensitivity_screen,
                                             init_state_prop[2] * sensitivity_screen])

            # Cost of Treatment = cost of Tx * (naturally found "I" + screened to be positive)
            c_cycle_treated = int(sum(p_prop_test_positive) * c_treatment) + init_state_prop[2] * 0.156 * c_treatment

            # Cost of Test: previous cycle init_state_prop * test cost
            c_cycle_test = int(sum(init_state_prop[0:3] * c_test))

        else:
            # No Test Conducted
            sensitivity_screen = 0
            specificity_screen = 0

            # New Cost of Treatment:
            # Natural probability of being detected in active state * cost of treatment
            c_cycle_treated = init_state_prop[2] * 0.156 * c_treatment

            # No Test is given --> Cost == 0
            c_cycle_test = 0

        # starting from 'Susceptible' state
        p_SD = p_BD
        p_SI = int(0)
        p_SE = p_SE
        p_SS = 1 - p_SE - p_SD - p_SI

        # starting from 'Latent TB' state
        p_ED = p_BD
        p_EI = p_EI
        p_ES = sensitivity_screen
        p_EE = 1 - p_ED - p_EI - p_ES

        # starting from 'Active TB' state (p_ED and p_ID are same: 0.0328)
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
        cycle_cost = c_cycle_test + c_cycle_treated

        # accumulate each cycle's "life-months" into "total_life_months"
        total_life_months += cycle_reward
        total_accum_cost += cycle_cost

specificity_screen = 0.95
sensitivity_screen = 0.8
c_test = 10
init_state_prop = np.array([1, 2, 3, 4])
test_array = init_state_prop[0:3] * c_test
test_array
sum(test_array)

p_prop_test_positive = np.array([init_state_prop[0] * (1 - specificity_screen),
                                             init_state_prop[1] * sensitivity_screen,
                                             init_state_prop[2] * sensitivity_screen])
c_cycle_treated_1 = int(sum(p_prop_test_positive * c_treatment)) + init_state_prop[
                2] * 0.156 * c_treatment
c_cycle_treated_2 = int(sum(p_prop_test_positive) * c_treatment) + init_state_prop[
                2] * 0.156 * c_treatment

c_cycle_treated_2 - c_cycle_treated_1
c_cycle_treated_1
n_max_cycles = 10
test_accum = 0
for t in range(0, n_max_cycles):
    test_accum += 1

test_accum