import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# Goal: creating a CEAC for screening at age 15 (screen == 3)

# 2. Run a simulation of 1000 cohorts under 1 WTP Threshold
WTP = 1000

def outcome_per_WTP(n_max_cycles=660, screen=100):
    """
    :param n_max_cycles: maximum number of cycles
    :param screen: number of simulation cycles
    :return:
    """
    total_life_months = 0
    total_accum_cost = 0

    # Starting Population
    # Proportion of "Susceptible" population
    start_prop_S = 1
    # proportion of "Latent" population
    start_prop_E = 0
    # proportion of "Active" population
    start_prop_I = 0
    # proportion of "Dead" population
    start_prop_D = 0
    # Starting Population Proportion as Array
    init_state_prop = np.array([start_prop_S, start_prop_E, start_prop_I, start_prop_D])

    for t in range(0, n_max_cycles):
        # Probability of Background Death
        p_BD = 1 - math.exp(-math.exp(-8 + t / 20) * 1 / 12)
        # Probability of State Transition
        # p(S->E)
        p_SE = np.random.beta(10, 6000)
        # p(E->I)
        p_EI = np.random.beta(0.7708, 9253)
        # p(I->D)
        p_ID = np.random.beta(20, 590)
        # p(I->E)
        p_IE = np.random.beta(20.78, 112.45)

        # Check When to Screen Every 60 Months (12 months * 5 years)
        if (t // 60) == screen and (t % 60) == 0:
            # Tested & Treated:
            sensitivity_screen = np.random.beta(40, 10)
            false_negative = 1 - sensitivity_screen
            specificity_screen = np.random.beta(38, 2)
            false_positive = 1 - specificity_screen

            # cost estimates
            c_test = np.random.gamma(40, 0.25)
            c_treatment = np.random.gamma(200, 1)

            # Probabilities
            p_SE = p_SE * specificity_screen  # probability that S --> I AND test correctly says does not have E/I
            p_EI = p_EI * false_negative  # probability that E --> I AND test has negative
            p_ES = sensitivity_screen  # among E, tested positive --> becomes S

            # Cost of Being Tested Positive and Treated
            # proportion of those being tested positive
            p_prop_test_positive = np.array([init_state_prop[0] * false_positive,
                                             init_state_prop[1] * sensitivity_screen])

            # Cost of Treatment = cost of Tx * (naturally found "I" + screened to be positive)
            c_cycle_treated = int(sum(p_prop_test_positive * c_treatment)) + init_state_prop[2] * p_IE * c_treatment

            # Cost of Test: previous cycle init_state_prop * test cost
            c_cycle_test = int(sum(init_state_prop[0:2] * c_test))

        else:
            # cost estimates
            c_treatment = np.random.gamma(200, 1)

            # Probabilities
            p_SE = p_SE
            p_EI = p_EI
            p_ES = 0
            p_IE = p_IE

            # Cost of Being Tested Positive and Treated
            # Cost of Treatment = cost of Tx * (naturally found "I")
            c_cycle_treated = init_state_prop[2] * p_IE * c_treatment
            c_cycle_test = 0

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

        if end_state_prop[3] == 1:
            break

        else:
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

    return total_life_months, total_accum_cost

def ICER_generator(intervention, comparator):
    """
    :param intervention:
    :param comparator:
    :return:
    """
    LM_intvn, Cost_intvn = outcome_per_WTP(n_max_cycles=660, screen = intervention)
    LM_comp, Cost_comp = outcome_per_WTP(n_max_cycles=660, screen=comparator)
    ICER = (Cost_intvn-Cost_comp)/(LM_intvn - LM_comp)
    return ICER

ICER_generator(3,1000)

def p_of_CE(max_WTP = 5000, simulation = 50, intervention = 3, comparator = 1000, seed = 123):

    """
    :param simulation: number of simulations
    :param threshold: WTP Threshold
    :return:
    """
    np.random.seed(seed)

    # creating an empty list
    outputs = []

    ls_WTP = list(range(0, max_WTP, 50))
    # for-loop to include WTP per output
    for i in ls_WTP:
        ls_ticker = []
        # for-loop to simulate & get proportion of CE per WTP
        for j in range(0, simulation):
            # get ICER of the WTP
            i_ICER = ICER_generator(intervention, comparator)
            # ticker = 1 if the WTP's ICER <= threshold 0 otherwise
            if i_ICER <= i:
                ticker = 1
            else:
                ticker = 0
            # store all ticker in a list for the WTP
            ls_ticker.append(ticker)
        # total number of positive ticker in the WTP
        n_of_positive = sum(ls_ticker)
        # total number of ticker in the WTP
        n_of_total = len(ls_ticker)
        # proportion of CE <= WTP
        p_of_CE = n_of_positive/n_of_total

        # store WTP and p_of_CE into outputs
        outputs.append((i,p_of_CE))

    # making the list of list into dataframe
    df_WTP_CE = pd.DataFrame(outputs, columns=['WTP', 'Probability'])

    return df_WTP_CE

def WTP_at_1000(WTP = 1000, simulation = 1000, intervention = 3, comparator = 1000, seed = 123):
    np.random.seed(seed)
    ls_ticker = []
    for j in range(0, simulation):
        # get ICER of the WTP
        i_ICER = ICER_generator(intervention, comparator)
        # ticker = 1 if the WTP's ICER <= threshold 0 otherwise
        if i_ICER <= WTP:
            ticker = 1
        else:
            ticker = 0
        # store all ticker in a list for the WTP
        ls_ticker.append(ticker)
    # total number of positive ticker in the WTP
    n_of_positive = sum(ls_ticker)
    # total number of ticker in the WTP
    n_of_total = len(ls_ticker)
    # proportion of CE <= WTP
    p_of_CE = n_of_positive / n_of_total
    return p_of_CE
