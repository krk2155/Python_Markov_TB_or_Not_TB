import math
import numpy as np

"""p_BD_month = 1-math.exp(-math.exp(-8+t/20)*1/12)
r_BD_month = -math.log(1 - p_BD_month)*60
p_BD_5yr = 1 - math.exp(-r_BD_month)"""

t = 0
n_max_cycles = 10
while t < n_max_cycles:
    # probability of background death
    p_BD_5yr = 1 - math.exp(-(-math.log(1 - (1-math.exp(-math.exp(-8+t/20)*1/12))*60)))

    #Transforming Monthly Prob --> Annual Prob
    #p(S->E)
    p_SE_month = 0.00167
    r_SE_month = -math.log(1 - p_SE_month)*60
    p_SE_5yr = 1- math.exp(-r_SE_month)
    #p(E->I)
    p_EI_month = 0.0000833
    r_EI_month = -math.log(1-p_EI_month)*60
    p_EI_5yr = 1-math.exp(-r_EI_month)
    #p(E->D)
    p_ED_month = 0.0328
    r_ED_month = -math.log(1-p_ED_month)*60
    p_ED_5yr = 1-math.exp(-r_ED_month)
    #p(I->D)
    p_ID_month = 0.0328
    r_ID_month = -math.log(1-p_ID_month)*60
    p_ID_5yr = 1-math.exp(-r_ID_month)
    #p(I->E)
    p_IE_month = 0.156
    r_IE_month = -math.log(1-p_IE_month)*60
    p_IE_5yr = 1-math.exp(-r_IE_month)

    p_BD_month = 1-math.exp(-math.exp(-8+t/20)*1/12)
    r_BD_month = -math.log(1 - p_BD_month)*60
    p_BD_5yr = 1 - math.exp(-r_BD_month)

    #State Transition Probabilities (per 1 month)
    #starting from 'Susceptible' state
    p_SD = 1 - math.exp(-(-math.log(1 - 1-math.exp(-math.exp(-8+t/20)*1/12))*60))
    p_SI = 0
    p_SE = p_SE_5yr
    p_SS = 1 - p_SE - p_SD
    #starting from 'Latent TB' state
    p_ED = 1 - math.exp(-(-math.log(1 - 1-math.exp(-math.exp(-8+t/20)*1/12))*60)) + p_ED_5yr
    p_EI = p_EI_5yr
    p_ES = 0
    p_EE = 1 - p_ED - p_EI - p_ES
    #starting from 'Active TB' state (p_ED and p_ID are same: 0.0328)
    p_IS = 0
    p_IE = p_IE_5yr
    p_ID = p_ED_5yr + 1 - math.exp(-(-math.log(1 - (1-math.exp(-math.exp(-8+t/20)*1/12)))*60))
    p_II = 1 - p_IE - p_ID
    #starting from 'dead' state
    p_DS = 0
    p_DE = 0
    p_DI = 0
    p_DD = 1

    # initial states
    init_state_prop =  np.array([1, 0, 0, 0])

    #transition probabilities
    transitionProb = np.array([[p_SS, p_SE, p_SI, p_SD],
                      [p_ES, p_EE, p_EI, p_ED],
                      [p_IS, p_IE, p_II, p_ID],
                      [p_DS, p_DE, p_DI, p_DD]
                     ])
    # end states
    end_state_prop = np.array([0, 0, 0, 0])
    end_state_prop = init_state_prop.dot(transitionProbMatrix)
    init_state_prop = end_state_prop
    sum(init_state_prop[0:3])

    # multiply initial states by transition probability to get end cycle states
    end_state_prop = init_state_prop.dot(transitionProbMatrix)
    # calculate the reward
    reward = sum(end_state_prop[0:3])
    total_reward += reward
    # each cycle: initial state --> end state;
    init_state_prop = end_state_prop
    # increment cycle
    t += 1
    # print(f"Cycle: {t}")
