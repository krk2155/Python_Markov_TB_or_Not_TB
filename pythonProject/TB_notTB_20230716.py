import math
import numpy as np


# Starting Population Proportion
# proportion of "Susceptible" population
start_prop_S = 1
# proportion of "Latent" population
start_prop_E = 0
# proportion of "Active" population
start_prop_I = 0
# proportion of "Dead" population
start_prop_D = 0

# Ending Population Proportion
# proportion of "Susceptible" population
end_prop_S = 0
# proportion of "Latent" population
end_prop_E = 0
# proportion of "Active" population
end_prop_I = 0
# proportion of "Dead" population
end_prop_D = 0

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

init_state_prop =  np.array([start_prop_S, start_prop_E, start_prop_I, start_prop_D])
end_state_prop =  np.array([end_prop_S, end_prop_E, end_prop_I, end_prop_D])

# Primers
t = 0
n_max_cycles = 240
total_reward_screen = 0
total_reward_no_screen = 0
switch_counter = 0
year_screen = 0
month_screen = 0
year_no_screen = 0
month_no_screen = 0

"""screening == TRUE"""
# Screening Switches
lets_screen = 0
switch = 5

while t < n_max_cycles:
    # probability of background death
    p_BD = 1 - math.exp(-math.exp(-8 + t / 20) * 1 / 12)
    if (t % 5) == 0:
        switch_counter += 1
    if switch_counter == switch:
        # SENSITIVITY OF TST TEST
        sens_TST = 0.80
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
        p_ID = p_ED + p_BD
        p_II = 1 - p_IE - p_ID

        # starting from 'dead' state
        p_DS = 0
        p_DE = 0
        p_DI = 0
        p_DD = 1
    else:
        # State Transition Probabilities (per 1 month)
        # starting from 'Susceptible' state
        p_SD = p_BD
        p_SI = 0
        p_SE = p_SE
        p_SS = 1 - p_SE - p_SD

        # starting from 'Latent TB' state
        p_ED = p_BD + p_ED
        p_EI = p_EI
        p_ES = 0
        p_EE = 1 - p_ED - p_EI - p_ES

        # starting from 'Active TB' state (p_ED and p_ID are same: 0.0328)
        p_IS = 0
        p_IE = p_IE
        p_ID = p_ED + p_BD
        p_II = 1 - p_IE - p_ID

        #starting from 'dead' state
        p_DS = 0
        p_DE = 0
        p_DI = 0
        p_DD = 1

    #transition probabilities
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
    cycle_reward = sum(init_state_prop[0:3])*(1/12)
    total_reward_screen += cycle_reward

    t += 1
    year_screen = t//12
    month_screen = t % 12
    print(f"Cycle: {t}"
          f"Age: {year_screen} Yr {month_screen} Mo, "
          f"Susceptible: {init_state_prop[0]:.4f}, "
          f"Latent TB: {init_state_prop[1]:.4f}, "
          f"Active TB: {init_state_prop[2]:.4f}, "
          f"Dead: {init_state_prop[3]:.4f}, "
          f"Current reward: {cycle_reward:.4f}, Total Reward: {total_reward_screen:.4f}")


# Screening == FALSE
while t < n_max_cycles:
    # probability of background death
    p_BD = 1 - math.exp(-math.exp(-8 + t / 20) * 1 / 12)

    # State Transition Probabilities (per 1 month)
    # starting from 'Susceptible' state
    p_SD = p_BD
    p_SI = 0
    p_SE = p_SE
    p_SS = 1 - p_SE - p_SD

    # starting from 'Latent TB' state
    p_ED = p_BD + p_ED
    p_EI = p_EI
    p_ES = 0
    p_EE = 1 - p_ED - p_EI - p_ES

    # starting from 'Active TB' state (p_ED and p_ID are same: 0.0328)
    p_IS = 0
    p_IE = p_IE
    p_ID = p_ED + p_BD
    p_II = 1 - p_IE - p_ID

    #starting from 'dead' state
    p_DS = 0
    p_DE = 0
    p_DI = 0
    p_DD = 1

    #transition probabilities
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
    cycle_reward = sum(init_state_prop[0:3])*(1/12)
    total_reward_no_screen += cycle_reward

    t += 1
    year_no_screen = t//12
    month_no_screen = t % 12
    print(f"Cycle: {t}"
          f"Age: {year_no_screen} Yr {month_no_screen} Mo, "
          f"Susceptible: {init_state_prop[0]:.4f}, "
          f"Latent TB: {init_state_prop[1]:.4f}, "
          f"Active TB: {init_state_prop[2]:.4f}, "
          f"Dead: {init_state_prop[3]:.4f}, "
          f"Current reward: {cycle_reward:.4f}, Total Reward: {total_reward_no_screen:.4f}")

# Difference in Years and Months
diff_years = year_screen - year_no_screen
diff_months = month_screen - month_no_screen
diff_total_reward = total_reward_screen - total_reward_no_screen
print(f"Difference in Years {diff_years} and Months {diff_months}")
print(f"Difference in months {diff_total_reward} ")
