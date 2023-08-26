import numpy as np
import scipy.stats as st
import math


def cost_life_month_model_dist(n_max_cycles=660, screen=100, simulation_cycle=1000, seed = 123):

    """
    :param n_max_cycles: maximum number of cycles
    :param screen: screen * 5 year old - age at which screening is done
    :param simulation_cycle = number of simulation cycles
    :param seed = seed for simulation
    :return: returns total reward
    """
    ls_life_years = []
    ls_cost = []
    np.random.seed(seed)
    for i in range(0, simulation_cycle):
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
        # converting life-months to life-years
        if total_life_months % 12 > 0:
            life_years = total_life_months // 12 + total_life_months % 12
        else:
            life_years = total_life_months // 12

        # appending each cycle reward and cost into a list
        ls_life_years.append(life_years)
        ls_cost.append(total_accum_cost)
    # mean total life-months & costs
    mean_total_life_years = np.mean(np.array(ls_life_years))
    mean_total_cost = np.mean(np.array(ls_cost))

    # upper and lower range of 95% CI life-months
    life_years_95_CI = st.t.interval(confidence=0.95, df=len(ls_life_years) - 1,
                                     loc=np.mean(ls_life_years),
                                     scale=st.sem(ls_life_years))

    # upper and lower range of 95% CI costs
    cost_95_CI = st.t.interval(confidence=0.95, df=len(ls_cost) - 1,
                               loc=np.mean(ls_cost),
                               scale=st.sem(ls_cost))

    return [mean_total_life_years, life_years_95_CI, mean_total_cost, cost_95_CI]



def difference_calculator_Cost(screening_cost, no_screening_cost):
    """
    :param screening_cost:
    :param no_screening_cost:
    :return:
    """
    diff_total_costs = screening_cost - no_screening_cost
    if diff_total_costs < 0:
        diff_total_costs_abs = abs(diff_total_costs)
        diff_total_costs = -diff_total_costs_abs
    else:
        diff_total_costs_abs = abs(diff_total_costs)
        diff_total_costs = diff_total_costs_abs

    print(f"Difference in Total Costs: {diff_total_costs:.5f} ")

    return round(diff_total_costs, 5)
