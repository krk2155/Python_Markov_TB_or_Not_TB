import numpy as np

def cost_life_month_model_dist(n_max_cycles=660, screen=100):
    """
    :param n_max_cycles: maximum number of cycles
    :param switch: decides at which point to conduct the screening;default at 10 (no-screen)
    :return: returns total reward
    """
    total_life_months = 0
    total_accum_cost = 0

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
        p_BD = np.random.beta(20, 590,1000)

        # Probability of State Transition
        # p(S->E)
        p_SE = np.random.beta(10, 6000)
        # p(E->I)
        p_EI = np.random.beta(0.7708, 9253)
        # p(E->D)
        p_ED = 0.0328
        # p(I->D)
        p_ID = 0.0328
        # p(I->E)
        p_IE = np.random.beta(20.78, 112.45)

        # cost estimates
        c_test = np.random.gamma(40, 0.25)
        c_treatment = np.random.gamma(200, 1)

        # Check When to Screen Every 60 Months (12 months * 5 years)
        if (t // 60) == screen and (t % 60) == 0:
            # Tested & Treated:
            sens_TST = np.random.beta(40, 10)
            false_positive_TST = np.random.beta(38, 2)

            # New Probability of Disease Progression
            p_SE = p_SE * (1 - false_positive_TST)
            p_EI = p_EI * (1 - sens_TST)
            p_IE = p_IE * (1 - sens_TST)

            # Cost of Test: previous cycle init_state_prop * test cost
            c_cycle_test = int(sum(init_state_prop[0:3] * c_test))

            # Cost of Being Tested Positive and Treated
            # proportion of those being tested positive
            p_prop_test_positive = np.array([init_state_prop[0] * false_positive_TST,
                                      init_state_prop[1] * sens_TST,
                                      init_state_prop[2] * sens_TST])
            c_cycle_treated = int(sum(p_prop_test_positive) * c_treatment)

        else:
            # No Test Conducted
            sens_TST = 0
            false_positive_TST = 0

            c_cycle_test = 0

            # New Probability of Disease Progression
            c_cycle_treated = init_state_prop[3] * p_IE * c_treatment

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

        for index, x in enumerate(end_state_prop):
            if x < 0:
                end_state_prop[index] = 0

        # new init_state is the old end_state
        init_state_prop = end_state_prop

        # add "life-month" of "Susceptible", "Latent TB", and "Active TB" states
        cycle_reward = sum(init_state_prop[0:3])
        cycle_cost = c_cycle_test + c_cycle_treated

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

    round(total_life_months, 2)
    round(total_accum_cost, 2)
    return [total_life_months, total_accum_cost]
