import threading
import math

tasks_per_thread = 10


def generate_threads(tasks: list, func):
    """Return list of non started threads
    :param tasks list of task - Arguments to be passed to the function func
    :param func func that will be fulfilled by thread
    :returns thread list (non started)
    """
    t_list = []  # List of created threads
    for i, task in enumerate(tasks):
        t = threading.Thread(target=func, name=f"thread {i}", args=(tasks[i], ))
        t_list.append(t)
    return t_list


def tasks_divider(tasks: list, tasks_per_thread=tasks_per_thread):
    groups_num = math.ceil(len(tasks) / tasks_per_thread)
    result = []
    for i in range(groups_num):
        result.append(tasks[i * tasks_per_thread: (i + 1) * tasks_per_thread])
    if result == []:
        result = [[]]
    return result
