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

def ICER_calculator(first_strategy, second_strategy):
    """
    This function takes first and second strategy, and then subtracts first strategy's life month
    from second strategy life month. Same applies to costs.
    This function then checks if incremental lifemonth is larger, smaller, or equal to 0. Same applies to incre_cost

    If Scenario1: incr_lm > 0 & incr_cost > 0 --> return
    If Scenario2: incr_lm > 0 & incr_cost < 0 --> return
    If Scenario3: incr_lm < 0 & incr_cost > 0 --> return
    If Scenario4: incr_lm < 0 & incr_cost < 0 --> return

    :param first_strategy[0]: life-month of the first strategy
    :param second_strategy[0]: life-month of the second strategy
    :param first_strategy[1]: cost of the first strategy
    :param second_strategy[1]: cost of the second strategy
    :return: ICER, dominant_strategy[life_month,cost]
    """
    # Incremental Life Month & Cost
    incr_lm = second_strategy[0] - first_strategy[0]
    incr_cost = second_strategy[1] - first_strategy[1]

    scenario = 0

    # Scenario 1 & 2
    if incr_lm > 0:
        if incr_cost > 0:
            ICER = incr_lm / incr_cost
            scenario = 1
            print(f"Scenario1: {ICER}")
            return [scenario, ICER, first_strategy, second_strategy]
        elif incr_cost < 0:
            ICER = incr_lm / incr_cost
            scenario = 2
            print(f"Scenario3: {ICER}")
            return [scenario, ICER, 0, second_strategy]

    # Scenario 3 & 4
    elif incr_lm < 0:
        if incr_cost < 0:
            ICER = incr_lm / incr_cost
            scenario = 3
            print(f"Scenario2: {ICER}")
            return [scenario, ICER, first_strategy, second_strategy]
        elif incr_cost > 0:
            ICER = incr_lm / incr_cost
            scenario = 4
            print(f"Scenario4: {ICER}")
            return [scenario, ICER, first_strategy, 0]

    elif incr_lm == 0:
        if incr_cost == 0:
            ICER = 0
            scenario = 5
            print(f"Scenario5,{ICER}")
            return [scenario, ICER, 0, 0]

def new_list_creator(list_of_strategies):
    """
    :param list_of_strategies: list of list of life-months and costs
    :return: "list_of_strategies_updated" or just "list_of_strategies" and "list_of_ICER"
    """
    t = 1
    ICER_1st_2nd_strategy = []
    list_of_ICER = []
    list_of_strategies_updated = []
    while t < 11:
        # ICER, first_strategy, second_strategy
        ICER_1st_2nd_scenario = ICER_calculator(list_of_strategies[t-1], list_of_strategies[t])

        # if incr_lm <0, and incr_cost>0, then remove first_strategy and ICER (Scenario == 4)
        if ICER_1st_2nd_scenario[0] == 4:
            list_of_strategies.remove(list_of_strategies[t - 1])
        # if incr_lm <0, and incr_cost>0, then

        # if incr_lm >0, and incr_cost>0, the

        # if incr_lm >0, and incr_cost<0, the

        # if second_strategy_LM < first_strategy_LM, then
            list_of_ICER.append(result[0])
            list_of_strategies_updated.append(ICER_1st_2nd_strategy[t - 1])
            list_of_strategies_updated.append(ICER_1st_2nd_strategy[t])
        if result[0] == 0:
            list_of_strategies_updated.append(list_of_strategies[t])
        # remove stage1
        elif result[1] == 0:
            list_of_strategies_updated.append(list_of_strategies[t-1])


        if result[0] != 0:
            list_of_ICER.append(result[0]) # add the new ICER to the list_of_ICER
        if result[1]:
            list_of_strategies_updated.append(list_of_strategies[t-1])
            list_of_strategies_updated.append(list_of_strategies[t])
        else:
            list_of_strategies_updated.append(list_of_strategies[t-1])
            list_of_strategies_updated.append(list_of_strategies[t])
        t +=1

    return list_of_ICER, list_of_strategies

def ICER_Comparator(list_of_ICER):
    """
    this function checks the second ICER and first ICER.
        If second ICER is SMALLER than first ICER:
            remove the second strategy (its LM and Cost)
            then, recalculate the ICER from where the second ICER was removed and make new ICER
        If second ICER is LARGER than first ICER:
            keep both first ICER And second ICER as they are
    :param list_of_ICER: NOT-sorted list of ICERS
    :return:
    """