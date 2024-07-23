from gurobipy import *
from load_data import LoadData
from i_TAREA_v1 import iTAREA

if __name__ == "__main__":
		
		i_tarea = iTAREA
		data_loader = LoadData
		#Loading problem information (infrastructure, application and problem information)
		nodes, rtt, num_nodes = data_loader.load_nodes('iTAREA/data/infrastructure_info.json')
		tasks, relation, num_tasks = data_loader.load_tasks('iTAREA/data/application_info.json')
		constraints, num_constraints, cpu_percentages, n_users = data_loader.load_problem_data('iTAREA/data/problem_definition.json', num_tasks)
		#Solving the problem
		i_tarea.solve (nodes, num_nodes, tasks, num_tasks, relation, constraints, num_constraints, cpu_percentages, n_users, rtt)