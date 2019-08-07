from pulp import *

# Define the problem
# Soduku
prob = LpProblem("Soduku", LpMaximize)

# Input
row = range(1,10)
col = range(1,10)
num = range(1,10)

# Decision variables
# Whether or not a 'num' should go into the set 'row' and 'col'
x = LpVariable.dicts("Board", (row, col, num), 0, 1, LpInteger)

# Given board
# https://krazydad.com/sudoku/sfiles/KD_Sudoku_EZ_8_v1.pdf
prob += x[1][1][2] == 1
prob += x[1][3][5] == 1
prob += x[1][6][7] == 1
prob += x[1][9][6] == 1

prob += x[2][1][4] == 1
prob += x[2][4][9] == 1
prob += x[2][5][6] == 1
prob += x[2][8][2] == 1

prob += x[3][5][8] == 1
prob += x[3][8][4] == 1
prob += x[3][9][5] == 1

prob += x[4][1][9] == 1
prob += x[4][2][8] == 1
prob += x[4][5][7] == 1
prob += x[4][6][4] == 1

prob += x[5][1][5] == 1
prob += x[5][2][7] == 1
prob += x[5][4][8] == 1
prob += x[5][6][2] == 1
prob += x[5][8][6] == 1
prob += x[5][9][9] == 1

prob += x[6][4][6] == 1
prob += x[6][5][3] == 1
prob += x[6][8][5] == 1
prob += x[6][9][7] == 1

prob += x[7][1][7] == 1
prob += x[7][2][5] == 1
prob += x[7][5][2] == 1

prob += x[8][2][6] == 1
prob += x[8][5][5] == 1
prob += x[8][6][1] == 1
prob += x[8][9][2] == 1

prob += x[9][1][3] == 1
prob += x[9][4][4] == 1
prob += x[9][7][5] == 1
prob += x[9][9][8] == 1

# Objective function
# Just searching for a feasible solution
prob += lpSum(1), "Objective"

# Constraints
# Each cell must contain only 1 digit
for r in row :
    for c in col :
        prob += lpSum(x[r][c][n] for n in num) == 1

# Each column must contain unique digits
for r in row :
    for n in num :
        prob += lpSum(x[r][c][n] for c in col) == 1

# Each row must contain unique digits
for c in col :
    for r in row :
        prob += lpSum(x[r][c][n] for n in num) == 1

# Each 3 x 3 block must contain all unique numbers
for i in range(1,10,3) :
    for j in range(1,10,3) :
        for n in num :
            prob += lpSum(x[r][c][n] for r in range(i,i+3) for c in range(j,j+3)) == 1

print(prob)

# Solve
prob.writeLP("soduku.lp")
prob.solve()

# Show output
print("Solver status: ", LpStatus[prob.status])
print("Objective function = ", value(prob.objective), "\n")

for var in prob.variables() :
    if (var.varValue == 1) :
        print(var.name, " = ", var.varValue)