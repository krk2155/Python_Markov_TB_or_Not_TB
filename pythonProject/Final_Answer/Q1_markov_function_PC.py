import numpy as np
import math


def life_month_model(n_max_cycles=660, screen=100):
    """
    :param n_max_cycles: maximum number of cycles
    :return: returns total reward
    """
    total_life_months = 0

    # Starting Population
    # proportion of "Susceptible" population
    start_prop_S = 1
    # proportion of "Latent" population
    start_prop_E = 0
    # proportion of "Active" population
    start_prop_I = 0
    # proportion of "Dead" population
    start_prop_D = 0

    init_state_prop = np.array([start_prop_S, start_prop_E, start_prop_I, start_prop_D])

    for t in range(0, n_max_cycles):
        # probability of background death
        p_BD = 1 - math.exp(-math.exp(-8 + t / 20) * 1 / 12)
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

            # Probabilities
            p_SE = specificity_screen * p_SE  # probability that S --> I AND test correctly says does not have E/I
            p_EI = false_negative * p_EI # probability that E --> I AND test has negative
            p_ES = sensitivity_screen # among E, tested positive --> becomes S

        else:
            # Probabilities
            p_SE = p_SE
            p_EI = p_EI
            p_ES = 0

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

        # accumulate each cycle's "life-months" into "total_life_months"
        total_life_months += cycle_reward

        year = t // 12
        month = t % 12

        # print cycle, age, proportion of "S","E","I","D", each cycle, and total reward
        print(f"Cycle: {t}, "
              f"Age: {year} Yr {month} Mo, "
              f"Susceptible: {init_state_prop[0]:.4f}, "
              f"Latent TB: {init_state_prop[1]:.4f}, "
              f"Active TB: {init_state_prop[2]:.4f}, "
              f"Dead: {init_state_prop[3]:.4f}, "
              f"Current reward: {cycle_reward:.4f}, Total Reward: {total_life_months:.4f}")

    return total_life_months


def difference_calculator_LM(screening_reward, no_screening_reward):
    """
    :param screening_reward:
    :param no_screening_reward:
    :return:year_month
    """
    diff_total_life_month = screening_reward - no_screening_reward
    if diff_total_life_month < 0:
        diff_life_year = abs(diff_total_life_month) // 12
        diff_life_year = -diff_life_year
        diff_remain_months = abs(diff_total_life_month) % 12
        diff_remain_months = -diff_remain_months
    else:
        diff_life_year = diff_total_life_month // 12
        diff_remain_months = diff_total_life_month % 12
    year_month = [round(diff_life_year, 4), round(diff_remain_months, 4)]

    print(f"Difference in Years {diff_life_year:.5f} and Months {diff_remain_months:.5f}")
    print(f"Difference in Total Months {diff_total_life_month:.5f} ")

    return year_month
