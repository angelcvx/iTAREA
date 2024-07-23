from gurobipy import *
from load_data import LoadData

class iTAREA:

	def solve (nodes, nNodes, tasks, nTask, relation,  constraints,  nConstraints, cpuPercentages, nUsers, rtt):

		solver = Model("milp") # Kind of solver used by Gurobi to obtain the solution (depends on the problem)
		solver.setParam(GRB.Param.NonConvex, 2) # Parameter to configure Gubori to solve the iTAREA

		# Defining problem variables to optimize
		communicationCost = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationCost')
		communicationCostDown = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationCostDown')
		computationCost = solver.addVar(vtype=GRB.CONTINUOUS, name='computationCost')
		communicationTime = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationTime')
		computationTime = solver.addVar(vtype=GRB.CONTINUOUS, name='computationTime')
		cores = solver.addVar(vtype=GRB.INTEGER, name='cores')

		assignment = [ [ solver.addVar(vtype=GRB.BINARY, name="ASING_%s_%s" % (r,c)) for c in range(nNodes) ] 
			for r in range(nTask*nUsers) ]

		# {node, % core assigned to task}
		percentageCPU = [ [ solver.addVar(vtype=GRB.INTEGER, name="pCPU_%s_%s" % (r,c), lb=0, ub=cpuPercentages*nodes[r][14]) for c in range(nTask) ] 
		for r in range(nNodes) ]

		# {node, % core assigned to task} This variable is used to avoid the division between variables (not supported by default)
		percentageCPUaux = [ [ solver.addVar(vtype=GRB.CONTINUOUS, name="auxPCPU_%s_%s" % (r,c), lb=0, ub=cpuPercentages*nodes[r][14]) for c in range(nTask) ] 
		for r in range(nNodes) ]

		for t in range(nTask): 
			solver.addConstr(quicksum(assignment[t][n] for n in range(nNodes)) == 1)
			for n in range(nNodes):
				solver.addConstr(((assignment [t][n])*(tasks[t][4] <= nodes[n][8]) *  (tasks[t][5] <= nodes[n][9]) * (tasks[t][3] <= nodes[n][1]) * (tasks[t][8] == nodes[n][10]) * ((tasks[t][7] == 'none') or (tasks[t][7] == nodes[n][11])) == assignment[t][n]))
				solver.addConstr(percentageCPU[n][t] == percentageCPU[n][t]*assignment[t][n])

		for n in range(nNodes):
			for t in range(nTask):
				solver.addConstr((percentageCPU[n][t]*percentageCPUaux[n][t]) == assignment[t][n])

		for m in range(nNodes):
			solver.addConstr(quicksum(percentageCPU[m]) <= cpuPercentages*nodes[m][14])
			solver.addConstr(quicksum(assignment[t][m] * tasks[t][1] for t in range(nTask)) <= nodes[m][4]) #Checking RAM

		for c in range(nConstraints):
			solver.addConstr( communicationTime == quicksum(quicksum(quicksum(assignment[constraints[c][i]][m]*(1-assignment[constraints[c][j]][m])*(((relation[constraints[c][i]][constraints[c][j]]*1000000)/nodes[m][1])+(rtt[0][0]*1000000)) for j in range(2, 2 + constraints[c][1]))  for i in range(2, 2 + constraints[c][1]))  for m in range(nNodes)))
			solver.addConstr( computationTime == quicksum(quicksum((assignment[constraints[c][i]][m]*((tasks[constraints[c][i]][0]*1000000)*(percentageCPUaux[m][constraints[c][i]])*nodes[m][14]*cpuPercentages))/nodes[m][0] for i in range(2, 2 + constraints[c][1]))  for m in range(nNodes)))
			solver.addConstr( (computationTime + communicationTime) <= (constraints[c][0]*1000000))

		solver.addConstr(communicationCost ==  quicksum(quicksum(quicksum(assignment[i][m]*(1-assignment[j][m])*(nodes[m][2]*(relation[i][j]/nodes[m][1])*nodes[m][5]) for j in range(nTask)) for i in range(nTask)) for m in range(nNodes)))
		solver.addConstr(computationCost ==  quicksum(quicksum(assignment[i][m]*((100-nodes[m][15])/100) * nodes[m][3] * ((tasks[i][0]*10000)/nodes[m][0]) for i in range(nTask)) for m in range (nNodes)))
		solver.addConstr(communicationCostDown ==  quicksum(quicksum(quicksum(assignment[i][m]*(1-assignment[j][m])*(nodes[m][6]*(relation[j][i]/nodes[m][7])*nodes[m][5]) for j in range(nTask)) for i in range(nTask)) for m in range(nNodes)))
		solver.addConstr(cores == quicksum(quicksum(percentageCPU[m][t] for t in range(nTask)) for m in range(nNodes)))

		solver.setObjectiveN(communicationCost + communicationCostDown + computationCost, 0, GRB.MINIMIZE)
		solver.setObjectiveN(cores, 1, GRB.MINIMIZE)


		solver.optimize()

		print('**** iTAREA v1.0 ****')
		if solver.status != 3:
			for v in solver.getVars():
				if v.varName[0:5] == 'ASING' and v.x == 1:
					aux = re.findall('\d+', v.varName)
					print('Task ' + str(aux[0]) + ' ('+ tasks[int(aux[0])][10] + ') assigned to Node ' + str(aux[1]))
				if str(v.varName[0:4]) == 'pCPU' and v.x > 0:
					aux = re.findall('\d+', v.varName)
					print('CPU assigned in Node ' + str(aux[0]) + ' to Task ' + str(aux[1]) + '. CPU (cores): ' + str(int(v.x)/(cpuPercentages)))
		else:
			print('The model is infeasible')

