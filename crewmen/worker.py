from crewmen.task import Task
import uuid

class CPU:
    def __init__(self, cores):
        self.cores = cores
        self.cores_used = 0

    def can_use(self, cores):
        if self.cores - self.cores_used >= cores:
            return True
        else:
            return False

    def use(self, cores):
        if self.can_use(cores):
            self.cores_used += cores
            return self.cores_used
        else:
            return -1

class Memory:
    def __init__(self, size):
        self.size = size
        self.size_used = 0

    def can_use(self, size):
        if self.size - self.size_used >= size:
            return True
        else:
            return False

    def use(self, size):
        if self.can_use(size):
            self.size_used += size
            return self.size_used
        else:
            return -1

class Disk:
    def __init__(self, size):
        self.size = size
        self.size_used = 0

    def can_use(self, size):
        if self.size - self.size_used >= size:
            return True
        else:
            return False

    def use(self, size):
        if self.can_use(size):
            self.size_used += size
            return self.size_used
        else:
            return -1

class Worker:
    def __init__(self, id = "w_" + uuid.uuid4().hex[:6]):
        # Meta Data
        self.id = id
        # Resources
        self.cpu: CPU = CPU(4)
        self.memory: Memory = Memory(1024)
        self.disk: Disk = Disk(4096)
        # Deployments
        self.deployments: list[Task] = []

    def can_deploy_task(self, task: Task):
        is_cpu_enough: bool = self.cpu.can_use(task.cpu_required) 
        is_memory_enough: bool = self.memory.can_use(task.memory_required) 
        is_disk_enough: bool = self.disk.can_use(task.disk_required) 

        return is_cpu_enough and is_memory_enough and is_disk_enough

    def deploy_task(self, task: Task):
        if self.can_deploy_task(task):
            # Consume Resources
            self.cpu.use(task.cpu_required)
            self.memory.use(task.memory_required)
            self.disk.use(task.disk_required)
            # Deploy the task
            self.deployments.append(task)
        else:
            print("deployment failed: not enough resources!")
            return None