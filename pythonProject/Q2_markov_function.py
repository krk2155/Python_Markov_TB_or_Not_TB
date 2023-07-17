import numpy as np
import math



def cost_life_month_model(n_max_cycles=600, screen=100):
    """
    :param n_max_cycles: maximum number of cycles
    :param switch: decides at which point to conduct the screening;default at 10 (no-screen)
    :return: returns total reward
    """
    total_life_months = 0
    total_accum_cost = 0

    # cost estimates
    c_test = 10
    c_treatment = 200

    # Starting Population Proportion
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
        p_SE = 0.00167
        # p(E->I)
        p_EI = 0.0000833
        # p(E->D)
        p_ED = 0.0328
        # p(I->D)
        p_ID = 0.0328
        # p(I->E)
        p_IE = 0.156

        # Check When to Screen Every 60 Months (12 months * 5 years)
        if (t // 60) == screen and (t % 60) == 0:
            # Tested & Treated:
            sens_TST = 0.80
            false_positive_TST = 0.05
            p_being_treated_by_test = sens_TST + false_positive_TST

            # Probability of Being Tested Positive
            p_being_treated_by_test = sens_TST + false_positive_TST

            # New Probability of Disease Progression
            p_SE = p_SE * (1- p_being_treated_by_test)
            p_EI = p_EI * (1- p_being_treated_by_test)

            # Cost of Test
            c_cycle_test = int(sum(init_state_prop[0:3] * c_test))

            # Cost of Being Tested Positive and Treated
            c_cycle_tested_treated = int(sum(init_state_prop[0:3] * p_being_treated_by_test * c_treatment))


        else:
            sens_TST = 0
            # Not-Tested & Treated:
            p_not_tested_treated = p_IE
            c_being_treated = p_being_treated_by_test * c_treatment + p_natural_treat*c_treatment

        # State Transition Probabilities (per 1 month)
        # starting from 'Susceptible' state
        p_SD = p_BD
        p_SI = int(0)
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

        # add "life-month" of "Susceptible", "Latent TB", and "Active TB" states
        cycle_reward = sum(init_state_prop[0:3])
        cycle_cost = p_TST_treat * c_treatment + c_being_tested

        # accumulate each cycle's "life-months" into "total_life_months"
        total_life_months += cycle_reward
        total_accum_cost += cycle_cost

        year = t // 12
        month = t % 12

        # print cycle, age, proportion of "S","E","I","D", each cycle, and total reward
        print(f"Cycle: {t}, "
              f"Age: {year} Yr {month} Mo, "
              f"Susceptible: {init_state_prop[0]:.4f}, "
              f"Latent TB: {init_state_prop[1]:.4f}, "
              f"Active TB: {init_state_prop[2]:.4f}, "
              f"Dead: {init_state_prop[3]:.4f}, "
              f"Total Reward: {total_life_months:.4f}, "
              f"Total Cost: {total_accum_cost:.4f}")

    return total_life_months


def difference_calculator(screening_reward_total_life_months, no_screening_total_life_months):
    """
    :param screening_reward:
    :param no_screening_reward:
    :return:year_month
    """
    diff_total_life_month = screening_reward_total_life_months - no_screening_total_life_months
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
