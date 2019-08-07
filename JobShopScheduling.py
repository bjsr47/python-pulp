# from pulp import *
from pulp import LpProblem, makeDict, LpVariable, LpMinimize,\
    LpInteger, lpSum, LpStatus, value

# Define the problem
# http://www.mit.edu/~jvielma/lectures/IAP2018/slides.pdf
# Assign n workers to complete m tasks
# At most one task per worker
# Assume n = 3, m = 2
prob = LpProblem("Job Shop", LpMinimize)

# Input
# Time it takes worker n to complete task m
timeInput = [[4, 3],
             [6, 5],
             [5, 6]]

# Worker and Task IDs
# Let's just use 0, 1, 2, etc... for this example
workers = range(len(timeInput))
tasks = range(len(timeInput[1]))

time = makeDict([workers, tasks], timeInput)

# Decision variables
# What worker is assigned to which task
x = LpVariable.dicts("WorkerToTask", (workers, tasks), 0, 1, LpInteger)

# Objective function
# Minimize the total time worked
prob += lpSum([time[w][t] * x[w][t] for w in workers for t in tasks]), "Objective"

# Constraints
# Each task must have one worker
for t in tasks :
    prob += lpSum(x[w][t] for w in workers) == 1, "Task"+str(t)

# Each worker can only have at most one task
for w in workers :
    prob += lpSum(x[w][t] for t in tasks) <= 1, "Worker"+str(w)

print(prob)

# Solve
prob.writeLP("jobShop.lp")
prob.solve()

# Show output
print("Solver status: ", LpStatus[prob.status])
print("Objective function = ", value(prob.objective), "\n")

for var in prob.variables() :
    print(var.name, " = ", var.varValue)