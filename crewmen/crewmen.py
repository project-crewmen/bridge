class Crewmen:
    def __init__(self):
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