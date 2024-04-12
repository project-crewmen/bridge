from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen
from crewmen.affinity_cost import AffinityCost

from data_structures.graph import Graph

from utils.crewmen_utils import  find_task, find_worker
from utils.graph_visualization.graph_visializer import GraphVisulizer

class M3C:
     def __init__(self, workers: list[Worker], tasks: list[Task], worker_graph: WorkerGraph, task_affinity_graph: TaskAffinityGraph):
          self.workers = workers
          self.tasks = tasks
          self.worker_graph = worker_graph
          self.task_affinity_graph = task_affinity_graph
     
     def run(self):
          wm = Crewmen()

          # Save previous deployment
          previous_deployment = GlobalDeployment(f"previous_deployment")

          for w in self.workers:
               t_ids = w.get_deployment_ids()
               for t in t_ids:
                    previous_deployment.record_deployment(w.id, t)

          # print("previous_deployment", previous_deployment)

          # Create a new deployment
          m3c_deployment = GlobalDeployment(f"m3c_deployment")

          for w in self.workers:
               t_ids = w.get_deployment_ids()
               for t in t_ids:
                    m3c_deployment.record_deployment(w.id, t)

          # print("m3c_deployment", m3c_deployment)


          # Constructing Task Graph (Node: Task, Edge: Affinity)
          task_graph = TaskGraph()

          for i in range(0, len(self.tasks)):
               for j in range(i, len(self.tasks)):
                    if i != j:
                         # Find Tasks
                         x_task = find_task(self.tasks, f"t_{i}")
                         y_task = find_task(self.tasks, f"t_{j}")

                         # Find Affinity Cost
                         associated_affinity_cost =  AffinityCost(self.worker_graph, x_task, y_task, self.task_affinity_graph.network.get_edge_weight(x_task.id, y_task.id))

                         if x_task and y_task and associated_affinity_cost:
                              task_graph.add_affinity_cost(x_task, y_task, associated_affinity_cost)

          # print(task_graph)

          # gv1 = GraphVisulizer(task_graph.network.graph)
          # gv1.show()

          # Net Cost
          net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
          # print(net_cost)

          # Get Affinity Cost Threshold
          t = wm.affinity_cost_threshold(task_graph.network.get_weighted_edge_list())
          # print(t)

          # Calculate Hight Affinity Costs Set
          hacs = wm.high_affinity_costs_set(task_graph.network.get_weighted_edge_list(), t)
          # print(hacs)

          # x = {(u, v) for u, v, w in hacs}
          # print(x)
          # gv1.show(colored_edges=x, color='#FF0000')

          # M3C Algorithm
          # Create CTS Graph
          """
          1. Consider the CTS after graph coloring and the worker network (for link properties).
          """
          cts_graph = Graph()
          cts_graph.add_edges(hacs)

          # print(cts_graph)
          node_colors_map, node_colors = cts_graph.get_disconnected_sets() # Perform depth first search(DFS) for each disconnected set and assign a unique color for each disconnected set nodes
          # print(node_colors_map, node_colors)

          # gv_cts_graph = GraphVisulizer(cts_graph.graph)
          # gv_cts_graph.show(colored_nodes=node_colors)

          """
          2. Perform pruning with graph embedding for each colored subgraph. (disconnected sets)
          """
          for k, v in node_colors_map.items():
               edges = cts_graph.get_weighted_edge_list_for_nodes(v)

               """
               2.1 Sort the edges with decreasing order of weights
               """
               sorted_edges = sorted(edges, key=lambda x: x[-1], reverse=True)
               # print(sorted_edges)

               """
               2.2 Start pruning with the highest Affinity Cost edge of unvisited edges.
               """
               edge_visits = set() # Using a hash map since O(1) time complexity
               for e in sorted_edges:
                    colocatable_task_id = cts_graph.select_least_degree_node_for_edge(e)
                    colocatable_task = find_task(self.tasks, colocatable_task_id)                    

                    # print(colocatable_task)

                    """
                    2.2.1 Try to place the task in one of the associated workers on the edge by evaluating the node/worker resources using the value function.
                    """
                    deployed_worker_id = m3c_deployment.get_key_for_value(colocatable_task_id)                    
                    deployed_worker = find_worker(self.workers, deployed_worker_id)

                    worker_id_of_other_task = m3c_deployment.get_key_for_value(cts_graph.get_other_node(e, colocatable_task_id))                 
                    deployed_worker_of_other_task = find_worker(self.workers, worker_id_of_other_task)

                    # print("deployed_worker_id", deployed_worker_id, "worker_id_of_other_task", worker_id_of_other_task)

                    if(deployed_worker_of_other_task and deployed_worker_of_other_task.can_deploy_task(colocatable_task)):
                         """
                         2.2.1.1. If value function allow the colocation of the task, then place it on the worker and mark the edge as visited.
                         """
                         # Colocate the task
                         deployed_worker.remove_task(colocatable_task)
                         deployed_worker_of_other_task.deploy_task(colocatable_task)
                         m3c_deployment.colocate_deployment(colocatable_task_id, deployed_worker_id, worker_id_of_other_task)

                         # print(m3c_deployment)
                    else:
                         """
                         2.2.1.2. If value function not allow the colocation of the task, then consider the worker network.
                         Get the least weighted edge of associated edges of the workers of the tasks and try to place the task at a worker.
                         Repeat the process until possible worker found.
                         """
                         neighbors = self.worker_graph.network.get_weighted_edge_list_for_nodes([worker_id_of_other_task])
                         sorted_neighbors = sorted(neighbors, key=lambda x: x[-1], reverse=False)
                         
                         # print(sorted_neighbors)

                         for nei in sorted_neighbors:
                              deployed_worker_of_other_task = find_worker(self.workers, nei[1])

                              if(deployed_worker_of_other_task and deployed_worker_of_other_task.can_deploy_task(colocatable_task)):
                                   # Colocate the task
                                   deployed_worker.remove_task(colocatable_task)
                                   deployed_worker_of_other_task.deploy_task(colocatable_task)
                                   m3c_deployment.colocate_deployment(colocatable_task_id, deployed_worker_id, worker_id_of_other_task)

                                   # print("deployed oiiiii", m3c_deployment)
                                   break
                              else:
                                   # print("cant")
                                   continue


          # print(m3c_deployment)

          # Constructing Task Graph (Node: Task, Edge: Affinity)
          m3c_task_graph = TaskGraph()

          for i in range(0, len(self.tasks)):
               for j in range(i, len(self.tasks)):
                    if i != j:
                         # Find Tasks
                         x_task = find_task(self.tasks, f"t_{i}")
                         y_task = find_task(self.tasks, f"t_{j}")

                         # Find Affinity Cost
                         associated_affinity_cost =  AffinityCost(self.worker_graph, x_task, y_task, self.task_affinity_graph.network.get_edge_weight(x_task.id, y_task.id))

                         if x_task and y_task and associated_affinity_cost:
                              m3c_task_graph.add_affinity_cost(x_task, y_task, associated_affinity_cost)

          # Net Cost
          m3c_net_cost = wm.net_cost(m3c_task_graph.network.get_weighted_edge_list())
          # print(m3c_net_cost)

          return m3c_deployment, m3c_net_cost



                    

          


     

     