import numpy as np
import math

def cost_life_month_model_dist(n_max_cycles = 660, screen = 100, simulation_cycle = 1000):
    """
    :param n_max_cycles: maximum number of cycles
    :return: returns total reward
    """

    ls_life_month = []
    ls_cost = []
    for i in range(simulation_cycle):
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
            p_BD = 1 - math.exp(-math.exp(-8 + t / 20) * 1 / 12)

            # Probability of State Transition
            # p(S->E)
            p_SE = np.random.beta(10, 6000)
            # p(E->I)
            p_EI = np.random.beta(0.7708, 9253)
            # p(E->D)
            p_ED = np.random.beta(20, 590)
            # p(I->D)
            p_ID = np.random.beta(20, 590)
            # p(I->E)
            p_IE = np.random.beta(20.78, 112.45)

            # cost estimates
            c_test = np.random.gamma(40, 0.25)
            c_treatment = np.random.gamma(200, 1)

            # Check When to Screen Every 60 Months (12 months * 5 years)
            if (t // 60) == screen and (t % 60) == 0:
                # Tested & Treated:
                sensitivity_screen = np.random.beta(40, 10)
                specificity_screen = np.random.beta(38, 2)

                # New Probability of Disease Progression
                # [assuming mutual exclusivity between p_EI and positive test results]
                p_SE = p_SE - specificity_screen
                p_EI = p_EI - (1 - sensitivity_screen)
                p_IE = p_IE + sensitivity_screen

                # Cost of Being Tested Positive and Treated
                # proportion of those being tested positive
                p_prop_test_positive = np.array([init_state_prop[0] * (1-specificity_screen),
                                                 init_state_prop[1] * sensitivity_screen,
                                                 init_state_prop[2] * sensitivity_screen])

                # Cost of Treatment = cost of Tx * (naturally found "I" + screened to be positive)
                c_cycle_treated = int(sum(p_prop_test_positive) * c_treatment) + init_state_prop[2] * p_IE * c_treatment

                # Cost of Test: previous cycle init_state_prop * test cost
                c_cycle_test = int(sum(init_state_prop[0:3] * c_test))

            else:
                # No Test Conducted
                sensitivity_screen = 0
                specificity_screen = 0

                # New Cost of Treatment:
                # Natural probability of being detected in active state * cost of treatment
                c_cycle_treated = init_state_prop[2] * p_IE * c_treatment

                # No Test is given --> Cost == 0
                c_cycle_test = 0

            # starting from 'Susceptible' state
            p_SD = p_BD
            p_SI = int(0)
            p_SE = p_SE
            p_SS = 1 - p_SE - p_SD - p_SI

            # starting from 'Latent TB' state
            p_ED = p_BD + p_ED
            p_EI = p_EI
            p_ES = sensitivity_screen
            p_EE = 1 - p_ED - p_EI - p_ES

            # starting from 'Active TB' state (p_ED and p_ID are same: 0.0328)
            p_IS = 0
            p_IE = p_IE
            p_ID = p_ID + p_BD
            p_II = 1 - p_IE - p_ID - p_IS

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

        # appending each cycle reward and cost into a list
        ls_life_month.append(total_life_months)
        ls_cost.append(total_accum_cost)
    mean_total_life_month = np.mean(np.array(ls_life_month))
    mean_total_cost = np.mean(np.array(ls_cost))
    upper_life_month = np.percentile(np.array(ls_life_month), 97.5)
    lower_life_month = np.percentile(np.array(ls_life_month), 2.5)
    upper_cost = np.percentile(np.array(ls_cost), 97.5)
    lower_cost = np.percentile(np.array(ls_cost), 2.5)
    print(f"Avg. LM: {mean_total_life_month:.2f}, 95% CI: ({upper_life_month:.2f}, {lower_life_month:.2f}), "
          f"Avg. Cost: {mean_total_cost:.2f}, 95% CI: ({upper_cost:.2f}, {lower_cost:.2f}), "
          f"Screen: {screen * 5} Year Olds")

    return [mean_total_life_month, upper_life_month, lower_life_month, mean_total_cost, upper_cost, lower_cost]
