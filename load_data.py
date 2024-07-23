import json

class LoadData:

    #Reads node information from a JSON file and stores it in a 2D array.
    def load_nodes(file_path):

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            num_nodes = len(data)

            # Create the 2D array to contain the information of the nodes, and the round trip time (RTT) between nodes
            nodes = [[0 for i in range(17)] for u in range(num_nodes)]
            rtt = [[ 0 for c in range(num_nodes) ] for r in range(num_nodes)]

            # Defining each node that forms the infrastructure
            # 0 - CPU (cycles per second)
            # 1 - Bandwidth up (bits/s)
            # 2 - Power Upload (Ptx), 
            # 3 - Maximum energy consumption (Watts) 
            # 4 - RAM (Mb)
            # 5 - Importance of saving energy in nodes (real number between 0 and 1). In this case, all nodes has been configured with the same node weighting (1) 
            # 6 - Power Download (Prx), 
            # 7 - Bandwidth Down (bits/s), 
            # 8 - Sensing units (e.g., thermomether), '' if any 
            # 9 - Peripherals (e.g., GPU), '' if any
            # 10 - Type (e.g., sensing mote), 'computing' by default
            # 11- Location (e.g., dispatch 2.30),  
            # 12 - Owner (e,g., CAOSD group), 'public' by default
            # 13 - Communication capacities (e.g., wlan)
            # 14 - Number of cores, 
            # 15 - Percentage of idle energy consumption, 
            # 16 - Percentage of energy consumption in sleeping mode
        
            node_id = 0
            for key, node_data in data.items():
                nodes[node_id][0] = int(node_data.get("cpu", 0))
                nodes[node_id][1] = float(node_data.get("bandwidthUp", 0))
                nodes[node_id][2] = float(node_data.get("powerUpload", 0))
                nodes[node_id][3] = float(node_data.get("maxEnergyConsumption", 0))
                nodes[node_id][4] = int(node_data.get("ram", 0))
                nodes[node_id][5] = float(node_data.get("energySavingImportance", 0))
                nodes[node_id][6] = float(node_data.get("powerDownload", 0))
                nodes[node_id][7] = float(node_data.get("bandwidthDown", 0))
                nodes[node_id][8] = node_data.get("sensingUnits", "")
                nodes[node_id][9] = node_data.get("peripherals", "")
                nodes[node_id][10] = node_data.get("type", "computing")
                nodes[node_id][11] = node_data.get("location", "")
                nodes[node_id][12] = node_data.get("owner", "public")
                nodes[node_id][13] = node_data.get("communicationCapacities", "")
                nodes[node_id][14] = int(node_data.get("numberOfCores", 0))
                nodes[node_id][15] = float(node_data.get("idleEnergyConsumption", 0))
                nodes[node_id][16] = int(node_data.get("sleepingEnergyConsumption", 0))
                # Round trip time (s) between nodes. e.g., RTT between node 0 and 1: rtt[0][1]
                for timming in node_data.get("RTT", []):
                    rtt[node_id][int(timming.get("toNode"))-1] = float(timming.get("time"))   
                node_id += 1
                
            return nodes, rtt, node_id

        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{file_path}'")
            return None
        

    def load_tasks(file_path):

        #Loads task information from a JSON file into a 2D array.
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            num_tasks = len(data)
            # Create the 2D array
            tasks = [[0 for i in range(11)] for u in range(num_tasks)]
            relations = [[0 for i in range(num_tasks)] for u in range(num_tasks)]

            # Defining each task that forms the application:
            # 0 - CPU cycles, 
            # 1 - RAM required (mb), 
            # 2 - User (in case of replication for multiple users, 0 by default), 
            # 3 - Minimal transmission (in case of requiring a minimal bandwidtk (e.g., for video streaming in a specific quality)), 
            # 4 - Sensing requirements (e.g., thermometer), 
            # 5 - Peripheral requirements (e.g., camera, GPU), 
            # 6 - Transmit
            # 7 - Exact location (in case the app is located in a specific place (e.g., dispatch 4.1) 'none' by default), 
            # 8 - Type (e.g., sensing mote)
            # 9 - Disk required (Mb) 
            # 10 - Task name
            # (tasks[t][8] == nodes[n][10]) * ((tasks[t][7] == 'none') + (tasks[t][7] == nodes[n][11]))
            task_index = 0
            for task_id, task_data in data.items():
                tasks[task_index][0] = int(task_data.get("cpuCycles",0))
                tasks[task_index][1] = int(task_data.get("ramRequired", 0))
                tasks[task_index][2] = int(task_data.get("user", 0))
                tasks[task_index][3] = int(task_data.get("minimalTransmission", 0))
                tasks[task_index][4] = task_data.get("sensingRequirements", "")
                tasks[task_index][5] = task_data.get("peripheralRequirements", "")
                tasks[task_index][6] = int(task_data.get("transmit", 0))
                tasks[task_index][7] = task_data.get("exactLocation", "none")
                tasks[task_index][8] = task_data.get("type", "")
                tasks[task_index][9] = int(task_data.get("diskRequired", 0))
                tasks[task_index][10] = task_data.get("taskName", "")
                for transfer in task_data.get("dataTransfers", []):
                    relations[task_index][int(transfer.get("toTask"))-1] = int(transfer.get("dataAmount"))
                task_index += 1

            return tasks, relations, num_tasks

        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{file_path}'")
            return None
        

    def load_problem_data(file_path, num_tasks):

        #Loads problem information from a JSON file into a 2D array.
        try:
            with open(file_path, 'r') as file:
                problem_info = json.load(file)

            # Defining the time constratins (to assure the QoS).
            # 0 - max time to be executed
            # 1 - Number of tasks involved in the time constraint
            # 2...n - Index of the involved tasks
            # Example of time constraint. Max time, 0.5 seg. 3 tasks involved (0,1,2).
                # constraints[0][0] = 0.5
                # constraints[0][1] = 3
                # constraints[0][2] = 0
                # constraints[0][3] = 1
                # constraints[0][4] = 2
            
            num_constraints = len(problem_info.get("timeConstraints", []))
            constraints = [ [ 0 for c in range(num_tasks+2) ] for r in range(num_constraints) ]

            cpu_percentages = problem_info.get("cpuPercentages")
            n_users = problem_info.get("nUsers")
            constraint_id = 0
            for constraint in problem_info.get("timeConstraints", []):
                constraints[constraint_id][0] = float(constraint.get("completitionTime"))
                tasks_involved = constraint.get("tasksInvolved")
                constraints[constraint_id][1] = len(constraint.get("tasksInvolved"))
                aux = 0
                for task in tasks_involved:
                    constraints[constraint_id][aux+2] = int(task)-1
                    aux += 1
                constraint_id += 1
            return constraints, constraint_id, cpu_percentages, n_users

        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{file_path}'")
            return None
