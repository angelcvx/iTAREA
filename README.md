# iTAREA: Task-to-Node Allocator for Edge Computing

## Overview
iTAREA (Intelligent Task Allocation for Resource and Energy Awareness) is a Python-based tool designed to optimize the deployment of IoT applications in edge computing environments. It efficiently assigns tasks to nodes within heterogeneous infrastructures, ensuring optimal resource utilization and minimal energy consumption. iTAREA leverages a Mixed Integer Linear Programming (MILP) solver, Gurobi, to determine the best node for each task, specifying the required CPU, RAM, and disk resources to meet predefined Quality of Service (QoS) parameters.

## Key Features
- **Energy Efficiency**: Minimizes the overall energy consumption of applications while maintaining performance.
- **Resource Optimization**: Allocates CPU, RAM, and disk resources efficiently to handle multiple applications.
- **Multi-Tenancy Support**: Capable of managing resources in environments with multiple users and applications.
- **Integration with Containerization Technologies**: Designed to work seamlessly with Docker and Kubernetes, facilitating easy deployment and scalability.
- **Time and Resource Constraints Handling**: Considers inter-task communication times and partial CPU allocations to ensure timely and efficient task execution.

## Prerequisites
- **Python 3.x**: Ensure Python is installed on your system.
- **Gurobi Optimizer**: iTAREA uses Gurobi for solving the MILP problems. A valid Gurobi license is required.

## Configuration

Application and Infrastructure Information: Define your application and infrastructure in the /data folder using the provided JSON templates.
Adjusting Parameters: Modify the task execution times, number of users, and CPU portions in the configuration files as needed.
Data Folder Structure /data

- **application_info.json:** Contains details about the tasks of the application.
- **infrastructure_info.json:** Describes the nodes available in the infrastructure.
- **problem_definition.json:** Additional configuration files for time restrictions, user count, and CPU portions.

## Usage

Describe your application, infrastructure and problem using application_info.json, infrastructure_info.json, and problem_data.json in the /data folder.
Run iTAREA:
```bash
python main.py
```

## How it works 

The following equation [1] describes the operation of the iTAREA module:

![image](https://github.com/user-attachments/assets/5f7498c8-6ab6-4897-9e3b-5918d6c3a8ea)

![image](https://github.com/user-attachments/assets/5c299078-c804-4ac0-8937-65a15e5d351e)


## Citing iTAREA

If you use iTAREA in your research, please consider citing the following papers:

- [1] Angel Cañete, Mercedes Amor, Lidia Fuentes, "HADES: An NFV solution for energy-efficient placement and resource allocation in heterogeneous infrastructures," Journal of Network and Computer Applications, vol. 221, 2024. DOI: https://doi.org/10.1016/j.jnca.2023.103764.
- [2] Angel Cañete, Mercedes Amor, Lidia Fuentes, "Supporting IoT applications deployment on edge-based infrastructures using multi-layer feature models," Journal of Systems and Software, vol. 183, 2022. DOI: https://doi.org/10.1016/j.jss.2021.111086.
- [3] A. Cañete, M. Amor, and L. Fuentes, "Energy-Efficient Deployment of IoT Applications in Edge-Based Infrastructures: A Software Product Line Approach," IEEE Internet of Things Journal, vol. 8, no. 22, pp. 16427-16439, Nov. 2021. DOI: 10.1109/JIOT.2020.3030197
