#importing modules
import math
import numpy as np
import random

#parameters

#Background mortality (Monthly)
t=1
#Background mortality (5-yearly)
p_BD_month = 1-math.exp(-math.exp(-8+t/20)*1/12)
r_BD_month = -math.log(1 - p_BD_month)*60
p_BD_5yr = 1 - math.exp(-r_BD_month)

print(p_BD_5yr)
print(p_BD_month)

#Transforming Monthly Prob --> Annual Prob

#p(S->E)
p_SE_month = 0.00167
r_SE_month = -math.log(1 - p_SE_month)*60
p_SE_5yr = 1- math.exp(-r_SE_month)
print(p_SE_5yr)

#p(E->I)
p_EI_month = 0.0000833
r_EI_month = -math.log(1-p_EI_month)*60
p_EI_5yr = 1-math.exp(-r_EI_month)
print(p_EI_5yr)

#p(E->D)
p_ED_month = 0.0328
r_ED_month = -math.log(1-p_ED_month)*60
p_ED_5yr = 1-math.exp(-r_ED_month)
print(p_ED_5yr)

#p(I->D)
p_ID_month = 0.0328
r_ID_month = -math.log(1-p_ID_month)*60
p_ID_5yr = 1-math.exp(-r_ID_month)
print(p_ID_5yr)

#p(I->E)
p_IE_month = 0.156
r_IE_month = -math.log(1-p_IE_month)*60
p_IE_5yr = 1-math.exp(-r_IE_month)
print(p_IE_5yr)

#sensitivity of test
#p(test positive)/p(disease positive)
#-->p(I_tested->E) = 0.8
#-->p(E_tested->S) = 0.8


#each cycle (1 month)
i = 0
#year
t = 0

n_age_init = 0
n_age_max = 100
n_cycles = 12*(n_age_max - n_age_init)

c_test = 50
c_treatment = 200

#probability of background death
p_BD_month = 1-math.exp(-math.exp(-8+t/20)*1/12)
r_BD_month = -math.log(1 - p_BD_month)*60
p_BD_5yr = 1 - math.exp(-r_BD_month)

#Starting Population Proportion
#proportion of "Susceptible" population
start_prop_S = 1
#proportion of "Latent" population
start_prop_E = 0
#proportion of "Active" population
start_prop_I = 0
#proportion of "Dead" population
start_prop_D = 0

#Ending Population Proportion
#proportion of "Susceptible" population
end_prop_S = 0
#proportion of "Latent" population
end_prop_E = 0
#proportion of "Active" population
end_prop_I = 0
#proportion of "Dead" population
end_prop_D = 0

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

#defining the state variable
states = ["Susceptible","Latent TB","Active TB", "Dead"]

transitionProbMatrix =[[p_SS,p_SE,p_SI,p_SD],
                  [p_ES,p_EE,p_EI,p_ED],
                  [p_IS,p_IE,p_II,p_ID],
                  [p_DS,p_DE,p_DI,p_DD]
                 ]
s = [1, 0, 0]
p = np.array([[0.856,0.138,0.007],
    [0.000,0.982,0.018],
    [0.000,0.000,1.000]])
c=s*p
print(c)