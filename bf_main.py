from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.link import Link
from crewmen.affinity_cost import AffinityCost
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.crewmen import Crewmen

if __name__ == "__main__":
    wm = Crewmen()

    # Constructing Worker Graph (Node: Worker, Edge: Link)
    worker_graph = WorkerGraph()

    l1 = Link(response_time=0.01)
    l2 = Link(response_time=0.02)
    l3 = Link(response_time=0.03)

    w1 = Worker("w_1")
    w2 = Worker("w_2")
    w3 = Worker("w_3")
    
    worker_graph.add_link(w1, w2, l1)
    worker_graph.add_link(w1, w3, l2)
    worker_graph.add_link(w2, w3, l3)

    print("Worker Graph: ")
    # print(worker_graph.network.get_nodes(), "\n")
    # print(worker_graph.network.get_adjacency_matrix(worker_graph.network.get_nodes()), "\n")
    print(worker_graph.network.get_weighted_edge_list(), "\n")


    # Deploying Tasks on Workers
    deployment_map = {}

    def record_deployment(dict, k, v):
        if k in dict:
            dict[k].append(v)
        else:
            dict[k] = [v]
    
    t1 = Task("t_1")
    t2 = Task("t_2")

    w1.deploy_task(t1)
    record_deployment(deployment_map, w1.id, t1.id)
    w2.deploy_task(t2)
    record_deployment(deployment_map, w2.id, t2.id)

    print(deployment_map)


    # Constructing Task Graph (Node: Task, Edge: Affinity)
    task_graph = TaskGraph()

    ac1 = AffinityCost(worker_graph, t1, t2)
    task_graph.add_affinity_cost(t1, t2, ac1)
    
    print("\nTask Graph: ")
    # print(task_graph.network.get_nodes(), "\n")
    # print(task_graph.network.get_adjacency_matrix(task_graph.network.get_nodes()), "\n")
    print(task_graph.network.get_weighted_edge_list(), "\n")


    # Crewmen Monitoring Functions
    net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
    print("Net Cost: ", net_cost, "\n")
   