
import numpy as np
import math

def run_markov_chain(n_max_cycles=600, screen = 100):
    """
    :param n_max_cycles: maximum number of cycles
    :param switch: decides at which point to conduct the screening;default at 10 (no-screen)
    :return: returns total reward
    """
    total_reward = 0
    switch_counter = 0

    # Starting Population Proportion
    # proportion of "Susceptible" population
    start_prop_S = 1
    # proportion of "Latent" population
    start_prop_E = 0
    # proportion of "Active" population
    start_prop_I = 0
    # proportion of "Dead" population
    start_prop_D = 0

    init_state_prop = np.array([start_prop_S, start_prop_E, start_prop_I, start_prop_D])


    for t in range(0,n_max_cycles):
        # probability of background death
        p_BD = 1 - math.exp(-math.exp(-8 + t / 20) * 1 / 12)
        # SENSITIVITY OF TST TEST will turn on if screening == 1
        if (t // 60) == screen and (t % 60) == 0:
            sens_TST = 0.80
        else:
            sens_TST = 0
        # Transforming Monthly Prob --> Annual Prob
        # p(S->E)
        p_SE = 0.00167
        # p(E->I)
        p_EI = 0.0000833
        # p(E->D)
        p_ED = 0.0328
        # p(I->D)
        p_ID = 0.0328
        # p(I->E)
        p_IE = 0.156
        # State Transition Probabilities (per 1 month)
        # starting from 'Susceptible' state
        p_SD = p_BD
        p_SI = 0
        p_SE = p_SE
        p_SS = 1 - p_SE - p_SD

        # starting from 'Latent TB' state
        p_ED = p_BD + p_ED
        p_EI = p_EI
        p_ES = sens_TST
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
        if any(t < 0 for t in end_state_prop):
            break

        # new init_state is the old end_state
        init_state_prop = end_state_prop
        cycle_reward = sum(init_state_prop[0:3])
        total_reward += cycle_reward

        year = t // 12
        month = t % 12
        print(f"Cycle: {t}, "
              f"Age: {year} Yr {month} Mo, "
              f"Susceptible: {init_state_prop[0]:.4f}, "
              f"Latent TB: {init_state_prop[1]:.4f}, "
              f"Active TB: {init_state_prop[2]:.4f}, "
              f"Dead: {init_state_prop[3]:.4f}, "
              f"Current reward: {cycle_reward:.4f}, Total Reward: {total_reward:.4f}")
    return total_reward

def difference_calculator(screening_reward, no_screening_reward):
    """
    :param screening_reward:
    :param no_screening_reward:
    :return:year_month
    """
    diff_reward = screening_reward - no_screening_reward
    if diff_reward <0:
        diff_year = abs(diff_reward)//12
        diff_year = -diff_year
        diff_remain_months = abs(diff_reward) % 12
        diff_remain_months = -diff_remain_months
    else:
        diff_year = diff_reward // 12
        diff_remain_months = diff_reward % 12
    year_month = [round(diff_year, 4), round(diff_remain_months, 4)]
    print(f"Difference in Years {diff_year:.5f} and Months {diff_remain_months:.5f}")
    print(f"Difference in Total Months {diff_reward:.5f} ")

    return year_month