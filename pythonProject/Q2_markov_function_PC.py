import numpy as np
import math


def cost_life_month_model(n_max_cycles=660, screen=100):
    """
    :param n_max_cycles: maximum number of cycles
    :return: returns total reward
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

            # cost estimates
            c_test = 10
            c_treatment = 200

            # Probabilities
            # Probabilities
            p_SE = p_SE * specificity_screen  # probability that S --> I AND test correctly says does not have E/I
            p_EI = p_EI * false_negative # probability that E --> I AND test has negative
            p_ES = sensitivity_screen # among E, tested positive --> becomes S

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
            c_treatment = 200

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

        # stop the cycle when all individuals have died
        if end_state_prop[3] == 1:
            break
        # otherwise, check if any (S, E, I) are negative & continue
        else:
            for index, x in enumerate(end_state_prop):
                # if negative, turn the value into 0
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

    round(life_years, 4)
    round(total_accum_cost, 4)
    return [life_years, total_accum_cost]

def list_of_sorted_strategy():
    list_of_strategies = []
    # store the list of strategies into "list_of_strategies"
    for i in range(0, 11):
        list_of_strategies.append(cost_life_month_model(screen=i))

    # Adding "Do Nothing" Strategy (LM & Cost when screening is done at age 5000 (never screened))
    list_of_strategies.append(cost_life_month_model(screen=1000))

    # Adding index number (try: enumerate next time)
    # Note: Do Nothing has index number i == 11
    for i in range(0, len(list_of_strategies)):
        list_of_strategies[i].insert(0, '%d' % (i))

    # Sort the list in ascending order of Life-Years
    sorted_list_strategies = sorted(list_of_strategies, key=lambda x: x[1])

    return sorted_list_strategies



def ICER_calculator(first_strategy, second_strategy):
    """
    This function takes first and second strategy, and then subtracts first strategy's life year
    from second strategy life year. Same applies to costs.
    This function then checks if incremental life-year is larger, smaller, or equal to 0. Same applies to incre_cost

    If Scenario1: incr_ly > 0 & incr_cost > 0 --> return ICER (compare against WTP Threshold)
    If Scenario2: incr_ly > 0 & incr_cost < 0 --> 1st strategy dominated (remove 1st strategy)
    If Scenario3: incr_ly < 0 & incr_cost > 0 --> 2nd strategy dominated (remove 2nd strategy)
    If Scenario4: incr_ly < 0 & incr_cost < 0 --> return ICER (compare against WTP Threshold)

    :return: ICER, dominant_strategy[life_month,cost]
    """
    # Incremental Life Month & Cost
    incr_ly = second_strategy[1] - first_strategy[1]
    incr_cost = second_strategy[2] - first_strategy[2]

    # if 2nd Strategy's LY > 1st Strategy's LY
    if incr_ly > 0:
        # if 2nd Strategy's cost > 1st Strategy's cost
        if incr_cost > 0:
            ICER = incr_cost / incr_ly
            return ['%s' % f"{second_strategy[0]} vs. {first_strategy[0]}", ICER]
        # if 2nd Strategy's cost <= 1st Strategy's cost
        elif incr_cost <= 0:
            ICER = incr_cost / incr_ly
            return ['%s' % f"{second_strategy[0]} vs. {first_strategy[0]}", ICER,
                    'Remove: %s' % f"{first_strategy[0]}"]

    # if 2nd Strategy's LY < 1st Strategy's LY
    elif incr_ly < 0:
        # if 2nd Strategy's cost > 1st Strategy's cost
        if incr_cost < 0:
            ICER = incr_cost / incr_ly
            return ['%s' % f"{second_strategy[0]} vs. {first_strategy[0]}", ICER, 2]
        # if 2nd Strategy's cost <= 1st Strategy's cost
        elif incr_cost >= 0:
            ICER = incr_cost / incr_ly
            return ['%s' % f"{second_strategy[0]} vs. {first_strategy[0]}", ICER,
                    'Remove: %s' % f"{second_strategy[0]}"]

    # if 2nd Strategy's LY == 1st Strategy's LY
    elif incr_ly == 0:
        # if 2nd Strategy's cost > 1st Strategy's cost
        if incr_cost >= 0:
            return ['%s' % f"{second_strategy[0]} vs. {first_strategy[0]}",
                    'Remove: %s' % f"{second_strategy[0]}"]
        # if 2nd Strategy's cost <= 1st Strategy's cost
        elif incr_cost < 0:
            return ['%s' % f"{second_strategy[0]} vs. {first_strategy[0]}",
                    'Remove: %s' % f"{first_strategy[0]}"]

def print_ICER(sorted_list_strategies):
    list_of_ICERS = []
    for i in range(1, len(sorted_list_strategies)):
        list_of_ICERS.append(ICER_calculator(sorted_list_strategies[i - 1], sorted_list_strategies[i]))
    return list_of_ICERS

def strategy_remover(sorted_list_strategies, list_remove):
    new_list = []
    for e in sorted_list_strategies:
        if e[0] not in list_remove:
            new_list.append(e)
    return new_list