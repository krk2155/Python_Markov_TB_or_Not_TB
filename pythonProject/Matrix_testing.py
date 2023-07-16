import math
import numpy as np

t=0
#probability of background death
p_BD_month = 1-math.exp(-math.exp(-8+t/20)*1/12)
r_BD_month = -math.log(1 - p_BD_month)*60
p_BD_5yr = 1 - math.exp(-r_BD_month)

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

#State Transition Probabilities (per 1 month)
#starting from 'Susceptible' state
p_SD = p_BD_5yr
p_SI = 0
p_SE = p_SE_5yr
p_SS = 1 - p_SE - p_SD
#starting from 'Latent TB' state
p_ED = p_BD_5yr + p_ED_5yr
p_EI = p_EI_5yr
p_ES = 0
p_EE = 1 - p_ED - p_EI - p_ES
#starting from 'Active TB' state (p_ED and p_ID are same: 0.0328)
p_IS = 0
p_IE = p_IE_5yr
p_ID = p_ED_5yr + p_BD_5yr
p_II = 1 - p_IE - p_ID
#starting from 'dead' state
p_DS = 0
p_DE = 0
p_DI = 0
p_DD = 1



t=0
n_max_cycles = 10

init_state_prop =  [1, 0, 0, 0]
transitionProbMatrix = [[p_SS, p_SE, p_SI, p_SD],
                  [p_ES, p_EE, p_EI, p_ED],
                  [p_IS, p_IE, p_II, p_ID],
                  [p_DS, p_DE, p_DI, p_DD]
                 ]

end_state_prop = [0, 0, 0, 0]
total_cycle_matrix = [[0 for x in range(4)] for y in range(n_max_cycles)]

while t < n_max_cycles:
    # each cycle: initial state --> end state;
    # for each element in initial state
    for i in range(len(end_state_prop)):
        # for each COLUMN of the transition matrix
        for j in range(len(transitionProbMatrix[0])):
            # for each ROW of the transition matrix
            for k in range(len(transitionProbMatrix)):
                # multiply the initial state element by first column
                # add each multiplied value as one value and store as
                # first element in end row
                # I might have to use append function to include the multiplied value into the end_state_prop array
                #r_sum = 0
                end_state_prop[i] += init_state_prop[k] * transitionProbMatrix[k][j]
                #end_state_prop.insert(i,r_sum)
    # cycle reward
    # reward = sum all values in end_state_prop
    # make final "end_state_prop" as new "init_state_prop
    # init_state_prop = end_state_prop
    # do I want to make a total_cycle of matrix?
    # total_cycle_matrix[i][j] += init_state_prop[k] * transitionProbMatrix[k][j]
    t+=1
    #print(f"Cycle: {t}")

print(total_cycle_matrix)
print(init_state_prop[0])
print(transitionProbMatrix[0][0])
print(init_state_prop[0]*transitionProbMatrix[0][0])