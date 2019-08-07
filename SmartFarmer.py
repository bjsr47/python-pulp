from pulp import *

# Problem definition
# Maximize farmer's profit, see URL for problem description
# http://rutcor.rutgers.edu/~omyndyuk/lp354/08S/MT1sol.pdf
prob = LpProblem("Smart Farmer", LpMaximize)

# Input
crops = ["Corn", "Soybeans", "Oats"]
profitPerAcre = [17, 27, 39]
constraints = [[1, 9, 200],
               [1, 5, 250],
               [1, 10, 100]]
rhs = [10, 90, 2000]

# Decision variables
x = LpVariable.dict("Plant", crops, 0, None, LpContinuous)

# Objective function
profitPerAcre = makeDict([crops], profitPerAcre, 0)
prob += lpSum([x[c] * profitPerAcre[c] for (c) in crops]), "Profit"

# Constraints
coefficients = makeDict([crops, range(len(constraints))], constraints, 0)

for i in range(len(constraints)) :
    prob += lpSum(x[c] * coefficients[c][i] for c in crops) <= rhs[i], "#%s" % (i+1)

# Solve
prob.writeLP("farmer.lp")
prob.solve()

# Show output
print(prob)
print("Solver status: ", LpStatus[prob.status])
for var in prob.variables() :
    print(var.name, " = ", var.varValue)
print(value(prob.objective))