from crewmen.globaldeployment import GlobalDeployment

from typing import Dict

class Crewmen:
    def __init__(self):
        self.deployments_map: Dict[str, GlobalDeployment] = {}
        pass

    def affinity(self, m: int, d: float, m_x_y: int, d_x_y: float, w: float = 0.5):
        af_x_y = ((m_x_y/m)*w)+((d_x_y/d)*(1-w))
        return af_x_y
    
    def affinity_cost(self, af_x_y: float, l_x_y: float, amp: float = 1.0):
        ac_x_y = amp * af_x_y * l_x_y
        return ac_x_y

    def net_cost(self, ac_list):
        nc = sum(weight for _, _, weight in ac_list)
        return nc
    
    def affinity_cost_threshold(self, ac_list):
        avg_ac = self.net_cost(ac_list)/len(ac_list)
        return avg_ac
    
    def high_affinity_costs_set(self, ac_list, threshold: float):
        hacs = []
        for ac in ac_list:
            if(ac[2] >= threshold):
                hacs.append(ac)
        
        return hacs
    
    def get_colocatable_tasks_set(self, hacs: list[(str, str, float)]) -> list[str]:
        cts: list[str] = []

        for u, v, w in hacs:
            if u not in cts:
                cts.append(u)
            if v not in cts:
                cts.append(v)
        
        return cts

    def get_minimum_worker_subgraph_netcosts_list(self, worker_subgraph_netcost_list: Dict[str, float]):
        minimum_worker_subgraph_netcosts_list: Dict[str, float] = {}

        min_netcost = min(worker_subgraph_netcost_list.values())
        minimum_worker_subgraph_netcosts_list = {key: value for key, value in worker_subgraph_netcost_list.items() if value == min_netcost}

        return minimum_worker_subgraph_netcosts_list
    
    def get_best_possible_worker_arrangements(self, minimum_worker_subgraph_netcosts_list: Dict[str, float]):
        return list(minimum_worker_subgraph_netcosts_list.keys())
    
    def add_to_deployments_map(self, dep_id: str, dep: GlobalDeployment):
        self.deployments_map[dep_id] = dep
    
    def get_deployments_for_keys(self, keys: list[str]) -> list[GlobalDeployment]:
        return [self.deployments_map[key] for key in keys if key in self.deployments_map]
    
    def deployment_ratio(self, initial_netcost, current_netcost):
        return current_netcost / initial_netcost
    
    def network_optimization(self, dep_ratio):
        return 1 - dep_ratio